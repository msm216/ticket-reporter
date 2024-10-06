// 重置筛选条件并重新加载页面
function resetFilters(resetUrl) {
    // 获取表单元素
    // 设置默认日期和其他参数
    const defaultIssueSelect = 'all';
    const defaultStartDate = '2022-01-01';
    const defaultGroupingBy = 'none';
    // 构建重置后的 URL，传递查询参数需在视图函数中通过 request.args.get() 获取
    const resetParams = `?issue-select=${defaultIssueSelect}&start-date=${defaultStartDate}&group-by=${defaultGroupingBy}`;
    // 使用从模板中传递的 resetUrl 来重定向
    window.location.href = resetUrl + resetParams;
    console.log('Resetting filter...');
}

// 回到顶部的函数
function scrollToTop() {
    const scrollableContent = document.querySelector('.left-half');
    scrollableContent.scrollTop = 0; // 滚动到顶部
}