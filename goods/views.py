import os
import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.base import ContentFile
from .forms import ProductForm
from .models import Product

# Tripo3D 配置
TRIPO3D_API_KEY = "tsk_f2YGH3We5Y1p9k-677uj35Dxmlc0mtaVw0_GMugtaT7"
TRIPO3D_UPLOAD_URL = "https://api.tripo3d.ai/v2/openapi/upload"
TRIPO3D_TASK_URL = "https://api.tripo3d.ai/v2/openapi/task"
TRIPO3D_DOWNLOAD_URL = "https://api.tripo3d.ai/v2/openapi/download"


# 创建商品视图
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = request.user.shop_set.first()  # 假设每个用户有一个店铺
            product.save()
            form.save_m2m()
            return render(request, 'create_success.html')
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})


# 商品详情页视图
def good_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


# 创建 Tripo3D 模型视图
def create_tripo_model(request, pk):
    if request.method == 'POST':
        user=request.user
        user_coin=user.gold_coins
        if user_coin < 5:
            return JsonResponse({'success': False, 'message': '金币不足无法创建'})
        else:
            print(f'当前用户金额为{user_coin}')
            user.gold_coins-=5
            user.save()
            user_coin = user.gold_coins
            print(f'之后{user_coin}')
            try:
                product = Product.objects.get(pk=pk)

                if not product.image:
                    return JsonResponse({'success': False, 'message': '无法创建3D模型：商品没有图片。'})

                print("原始 image.name:", product.image.name)
                print("原始 image.path:", product.image.path)

                # 使用固定英文名上传，避免编码问题
                with product.image.open('rb') as f:
                    files = {
                        'file': ('upload.jpg', f, 'image/jpeg')
                    }
                    headers = {
                        'Authorization': f'Bearer {TRIPO3D_API_KEY}'
                    }

                    print("开始上传图片到 Tripo3D...")
                    upload_response = requests.post(TRIPO3D_UPLOAD_URL, headers=headers, files=files)
                    print("上传响应状态码：", upload_response.status_code)
                    print("上传响应内容：", upload_response.text)

                if upload_response.status_code != 200:
                    return JsonResponse({'success': False, 'message': '上传图片失败。'})

                upload_data = upload_response.json()
                file_token = upload_data.get('data', {}).get('image_token')

                if not file_token:
                    return JsonResponse({'success': False, 'message': '未获取到文件token。'})

                task_data = {
                    "type": "image_to_model",
                    "file": {
                        "type": "jpg",
                        "file_token": file_token
                    }
                }

                task_headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {TRIPO3D_API_KEY}"
                }

                print("开始创建3D模型任务...")
                task_response = requests.post(TRIPO3D_TASK_URL, headers=task_headers, json=task_data)
                print("任务响应状态码：", task_response.status_code)
                print("任务响应内容：", task_response.text)

                if task_response.status_code != 200:
                    return JsonResponse({'success': False, 'message': '3D建模任务创建失败。'})

                task_data = task_response.json()
                task_id = task_data.get('data', {}).get('task_id')

                if not task_id:
                    return JsonResponse({'success': False, 'message': '任务ID获取失败。'})

                product.tripo_task_id = task_id
                product.tripo_status = '生成中'
                product.save()

                return JsonResponse({'success': True, 'message': '3D模型已开始生成，请稍后刷新页面查看。'})

            except Exception as e:
                print("发生异常：", str(e))
                return JsonResponse({'success': False, 'message': f'创建失败：{str(e)}'})

    return JsonResponse({'success': False, 'message': '无效请求'})


# 查询模型生成状态并下载模型
def check_tripo_model_status(request, pk):
    try:
        product = Product.objects.get(pk=pk)

        if not product.tripo_task_id:
            return JsonResponse({'success': False, 'message': '未找到任务ID，无法查询状态。'})

        task_headers = {
            "Authorization": f"Bearer {TRIPO3D_API_KEY}"
        }

        # 查询任务状态
        task_status_response = requests.get(f"{TRIPO3D_TASK_URL}/{product.tripo_task_id}", headers=task_headers)
        print("任务状态查询响应：", task_status_response.status_code)
        print("任务状态查询响应内容：", task_status_response.text)
        print("任务状态查询响应内容json格式：", task_status_response.json())

        if task_status_response.status_code != 200:
            return JsonResponse({'success': False, 'message': '查询任务状态失败。'})

        task_status_data = task_status_response.json()
        task_status = task_status_data.get('data', {}).get('status')

        if task_status == 'success':
            # 模型已完成，获取下载路径
            download_url = task_status_data.get('data',{}).get('result', {}).get('pbr_model', {}).get('url', None)
            print(f"下载链接是{download_url}")
            if download_url:
                # 下载模型
                download_response = requests.get(download_url, headers=task_headers)

                if download_response.status_code == 200:
                    print('开始下载')
                    model_file_name = f"product_{product.pk}_3d_model.glb"  # 使用.glb格式
                    model_file_path = os.path.join('media',"3d_models", model_file_name)
                    recode_model_file_path=os.path.join("3d_models", model_file_name)
                    # 保存下载的文件
                    os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
                    with open(model_file_path, 'wb') as model_file:
                        model_file.write(download_response.content)
                    print('下载成功')
                    # 保存模型文件路径
                    product.tripo_3d_model = recode_model_file_path
                    product.tripo_status = '已完成'
                    product.save()

                    return JsonResponse({'success': True, 'message': '3D模型已下载并保存。'})

                else:
                    print('下载响应失败')
                    return JsonResponse({'success': False, 'message': '下载3D模型失败。'})

            else:
                print('未找到下载链接')
                return JsonResponse({'success': False, 'message': '没有找到下载链接。'})


        elif task_status == 'failed':

            return JsonResponse({'success': False, 'message': '3D模型生成失败。'})


        elif task_status == 'running':

            progress = task_status_data.get('data', {}).get('progress', 0)

            return JsonResponse({'success': True, 'message': str(progress)})


        else:

            return JsonResponse({'success': False, 'message': '未知状态。'})


    except Exception as e:
        print("发生异常：", str(e))
        return JsonResponse({'success': False, 'message': f'查询失败：{str(e)}'})



from django.shortcuts import render
from .models import Product  # 你的商品模型

def search_view(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query) if query else []
    print(f"query={query}, results={results}")
    return render(request, 'search_results.html', {'query': query, 'results': results})

# views.py

def category_view(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(category=query) if query else []
    return render(request, 'search_results.html', {'query': query, 'results': results})

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product  # 你应有这些模型
from commnents.models import Comment

def product_show(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments_qs = Comment.objects.filter(product=product).order_by('-created_at')
    paginator = Paginator(comments_qs, 10)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    return render(request, 'product_show.html', {
        'product': product,
        'comments': comments,
    })


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from commnents.models import Comment

@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Comment.objects.create(product=product, user=request.user, text=text)
    return redirect('goods:product_show', pk=product.id)
