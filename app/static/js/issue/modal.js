// 动态生成确认消息
function generateConfirmationMessage(formData) {
    let message = 'Please confirm your submission:\n\n';
    // 遍历 FormData 对象中的每个键值对
    formData.forEach((value, key) => {
        if (value) {  // 仅在值不为空时添加到消息中
            message += `${key.replace('_', ' ')}: ${value}\n`;  // 显示键值对，并用空格代替下划线
        }
        //console.log(key, value);
    });
    return message;
}

// 添加实例
function addIssue() {

    // 禁用默认的表单提交
    const formContent = document.getElementById('formContent');
    const formData = new FormData(formContent);  // 获取表单数据
    const confirmationMessage = generateConfirmationMessage(formData);
    // 确认提交内容
    confirmAction(confirmationMessage, function() {
        // 设置添加实例的路由
        const addUrl = `/${objectClass}/add`;
        console.log("Sending addInstance request to:", addUrl); // 检查 URL
        console.log("Form data:", Object.fromEntries(formData)); // 检查表单数据
        // 发起 AJAX 请求
        fetch(addUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'  // 确保后端可以识别这是一个 AJAX 请求
            }
        })
        .then(response => {
            console.log("Response status:", response.status); // 检查响应状态
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data); // 检查返回数据
            if (data.success) {
                // 显示成功信息并更新页面
                alert('Instance added successfully!');
                location.reload();  // 刷新页面或更新部分页面
            } else {
                // 显示错误信息
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An unexpected error occurred.');
        });
    });
}
