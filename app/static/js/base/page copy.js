document.addEventListener('DOMContentLoaded', function () {
    // 获取查询参数
    const queryParams = new URLSearchParams(window.location.search);
    // 打印所有查询参数
    queryParams.forEach((value, key) => {
        console.log(`${key}: ${value}`);
    });
    // 获取所有卡片对象
    const toggleButtons = document.querySelectorAll('.toggle-icon');
    // 展开收缩卡片
    toggleButtons.forEach(button => {
        const collapseElementId = button.getAttribute('data-target');
        const collapseElement = document.querySelector(collapseElementId);
        // Collapse show event
        collapseElement.addEventListener('show.bs.collapse', () => {
            button.querySelector('i').classList.remove('fa-chevron-down');
            button.querySelector('i').classList.add('fa-chevron-up');
        });
        // Collapse hide event
        collapseElement.addEventListener('hide.bs.collapse', () => {
            button.querySelector('i').classList.remove('fa-chevron-up');
            button.querySelector('i').classList.add('fa-chevron-down');
        });
    });
});


// 字符串首字母大写
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


// 开启模态框
function openModal(instanceId, modalMode, objectClass) {
    const moodalID = `${objectClass}${capitalizeFirstLetter(modalMode)}Modal`;
    console.log("Dynamic modal ID: ", moodalID);
    const modalModule = document.getElementById('modalModule');
        
    // 处理标题
    var titleActionSection = document.getElementById('titleActionSection');
    var titleObjectSection = document.getElementById('titleObjectSection');
    var titleIdSection = document.getElementById('titleIdSection');
    titleActionSection.textContent = modalMode ? capitalizeFirstLetter(modalMode) : 'Action';
    titleObjectSection.textContent = objectClass ? capitalizeFirstLetter(objectClass) : 'Object';
    titleIdSection.textContent = instanceId ? ` ${instanceId}` : '';
    
    // 获取按钮元素
    var modalSubmit = document.getElementById('modalSubmit');
    
    // 赋值隐藏元素
    document.getElementById('instId').value = instanceId || '';
    document.getElementById('modalMode').value = modalMode;
    console.log("Modal mode: ", document.getElementById('modalMode').value);

    // 传递参数到路由函数 load_form() 并获取返回的表单 HTML 内容
    fetch(`/load-form?modal-mode=${encodeURIComponent(modalMode)}&object-class=${encodeURIComponent(objectClass)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            // 把获取的 HTML 内容插入到id为 modalForm 的区块中
            document.getElementById('modalContent').innerHTML = data;
                        
            // 根据不同的 modalMode 动态设置 modalForm 的 action 路径
            var modalForm = modalModule.querySelector('.modal-form');
            modalForm.action = instanceId ? `/${objectClass}/${instanceId}/${modalMode}` : `/${objectClass}/${modalMode}`;
            console.log("Form action URL: ", modalForm.action);

            // 表单加载后显示模态框
            modalModule.style.display = "block";
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            console.error('Error loading form:', error);
        });
}


// 确认弹窗
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
        console.log('Action callback...');
    }
}


// 动态生成确认消息
function generateConfirmationMessage(formData) {
    // 初始确认消息文本
    let message = 'Please confirm your submission:\n\n';
    // 遍历 FormData 对象中的每个键值对
    formData.forEach((value, key) => {
        if (value) {  // 仅在值不为空时添加到消息中
            message += `${key.replace('_', ' ')}: ${value}\n`;  // 显示键值对，并用空格代替下划线
        }
    });
    return message;
}


// 添加实例
function addInstance(objectClass) {
    console.log('Adding', objectClass, instanceId);

    // 禁用默认的表单提交
    const form = document.getElementById('modalForm');
    const formData = new FormData(form);  // 获取表单数据
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


// 编辑实例
function editInstance(objectClass, instanceId) {
    console.log('Editing', objectClass, instanceId);

    const form = document.getElementById('modalForm');
    const formData = new FormData(form);
    const confirmationMessage = generateConfirmationMessage(formData);

    confirmAction(confirmationMessage, function() {
        fetch(`/${objectClass}/${instanceId}/edit`, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Instance edited successfully!');
                location.reload();
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An unexpected error occurred.');
        });
    });
}


function updateInstance(objectClass, instanceId) {
    console.log('Updating', objectClass, instanceId);
}


// 删除实例
function deleteInstance(objectClass, instanceId) {
    console.log('Deleting', objectClass, instanceId);
    // 确认删除操作
    confirmAction(`Are you sure you want to delete ${objectClass} instance ${instanceId}?`, function() {
        const deleteUrl = `/${objectClass}/${instanceId}/delete`;
        // 发起 AJAX 请求
        fetch(deleteUrl, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
    });
}


// 打印实例
function printInstance(objectClass, instanceId) {
    const printUrl = `/${objectClass}/${instanceId}/print`;
    window.open(printUrl, '_blank');
    console.log('Printing', objectClass, instanceId);
}


// 打印主题
function printTheme(objectClass) {
    const printUrl = `/${objectClass}/print/`;
    window.open(printUrl, '_blank');
    console.log('Printing', objectClass);
}



// 这里是 addInstance 的实现逻辑
function addInstance() {
    console.log('Adding instance...');
}

// 这里是 editInstance 的实现逻辑
function editInstance() {
    console.log('Editting modal...');
}

// 这里是 updateInstance 的实现逻辑
function updateInstance() {
    console.log('Updating instance...');
}