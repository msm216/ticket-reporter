function openIssueModal(mode, title, submitText) {
    const modal = document.getElementById('modalModule');
    const modalTitle = modal.querySelector('.modal-title');
    const submitButton = modal.querySelector('.modal-control .btn-primary');

    modalTitle.textContent = title || 'Default Title';
    submitButton.textContent = submitText || 'Submit';

    // 显示模态框
    modal.style.display = 'block';
}

// 重置筛选条件并重新加载页面
function resetFilters(resetUrl) {
    // 获取表单元素
    // 设置默认日期和其他参数
    const defaultStartDate = '2022-01-01';
    // 今天的日期
    const defaultEndDate = new Date().toISOString().split('T')[0];
    const defaultFilterBy = 'none';
    // 构建重置后的 URL
    const resetParams = `?start_date=${defaultStartDate}&end_date=${defaultEndDate}&filter-by=${defaultFilterBy}`;
    // 使用从模板中传递的 resetUrl 来重定向
    window.location.href = resetUrl + resetParams;
    console.log('Reset filter...');
}