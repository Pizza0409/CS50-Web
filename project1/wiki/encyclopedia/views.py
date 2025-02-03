from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
import random
from markdown2 import Markdown

markdowner = Markdown()

def index(request):
    if request.method == "POST":  # 當用戶提交表單時
        query = request.POST.get("q", "").strip()  # 獲取搜索內容，默認為空字串
        entries = util.list_entries()  # 獲取所有條目名稱

        search_results = []

        for entry in entries:
            if query.lower() == entry.lower():
                return HttpResponseRedirect(reverse("entry_page", args=[entry]))  # 使用 reverse
            elif query.lower() in entry.lower():
                search_results.append(entry)

        if search_results:
            return render(request, "encyclopedia/search_result.html", {
                "search_results": search_results
            })

        # 無匹配條目時，傳遞錯誤訊息到 error_page
        return HttpResponseRedirect(reverse("error_page"))

    entries = [entry for entry in util.list_entries() if entry.strip()]
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def entry_page(request, title):
    content = util.get_entry(title)

    if content is None:  # 如果條目不存在
        return render(request, "encyclopedia/error_page.html")

    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "content": markdowner.convert(content)
    })


def content_not_found(request):
    return render(request, "encyclopedia/error_page.html")

def search_result(request):
    return render(request, "encyclopedia/search_result.html")

def create_page(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        # 檢查條目標題是否已經存在
        if title in util.list_entries():
            return render(request, "encyclopedia/create_page.html", {
                "error": "The entry already exists. Please choose a different title."
            })

        # 保存新條目
        util.save_entry(title, content)

        # 重定向到新創建的條目頁面
        return HttpResponseRedirect(reverse("entry_page", args=[title]))

    return render(request, "encyclopedia/create_page.html")

def edit_page(request, title):
    # 預填寫內容
    pre_content = util.get_entry(title)

    if request.method == "POST":
        content = request.POST.get("content", "").strip()

        # 保存修改的條目
        util.save_entry(title, content)

        # 重定向到條目頁面
        return HttpResponseRedirect(reverse("entry_page", args=[title]))

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "pre_content": pre_content,
    })

def random_page(request):
    entries = util.list_entries()  # 確保調用方法以獲得所有條目
    a = random.randint(0, len(entries) - 1)  # 隨機選擇一個條目
    title = entries[a]

    # 嘗試獲取條目內容
    content = util.get_entry(title)

    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "content": markdowner.convert(content),
    })

