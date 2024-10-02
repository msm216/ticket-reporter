// 重置筛选条件并重新加载页面
function resetFilters(resetUrl) {
    // 获取表单元素
    // 设置默认日期和其他参数
    const defaultStartDate = '2022-01-01';
    const defaultFilterBy = 'none';
    // 构建重置后的 URL
    const resetParams = `?start_date=${defaultStartDate}&filterBy=${defaultFilterBy}`;
    // 使用从模板中传递的 resetUrl 来重定向
    window.location.href = resetUrl + resetParams;
    console.log('Reset filter...');
}