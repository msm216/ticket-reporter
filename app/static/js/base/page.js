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
function openModal(objectClass, instanceId, taskMode) {
    const modalId = `${objectClass}${capitalizeFirstLetter(taskMode)}Modal`;
    console.log("Dynamic modal ID: ", modalId);
    const modalModule = document.getElementById('modalModule');   // 获取模态框模块
    const formContent = document.getElementById('formContent');   // 获取表单内容区块
    // 设置标题
    document.getElementById('titleActionSection').textContent = taskMode ? capitalizeFirstLetter(taskMode) : 'Task';
    document.getElementById('titleObjectSection').textContent = objectClass ? capitalizeFirstLetter(objectClass) : 'Object';
    document.getElementById('titleIdSection').textContent = instanceId ? ` ${instanceId}` : '';
    // 设置隐藏字段
    document.getElementById('instId').value = instanceId || '';
    document.getElementById('taskMode').value = taskMode;
    console.log("Modal mode: ", document.getElementById('taskMode').value);
    // Step 1: 模板传递参数到路由函数 load_form() 并获取返回 HTML
    fetch(`/load-form?modal-mode=${encodeURIComponent(taskMode)}&object-class=${encodeURIComponent(objectClass)}`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to load form');
            return response.text();
        })
        .then(formHTML => {
            // 将获取到的表单内容插入到 id 为 formContent 的区块中
            formContent.innerHTML = formHTML;
            // Step 2: 如果是编辑模式，加载实例数据并填充表单
            if (taskMode === 'edit' && instanceId) {
                fetch(`/${objectClass}/${instanceId}`)
                    .then(response => {
                        if (!response.ok) throw new Error('Failed to fetch instance data');
                        return response.json();
                    })
                    .then(instanceData => {
                        console.log("Fetched instance data:", instanceData);
                        // 动态填充表单字段
                        for (const [key, value] of Object.entries(instanceData)) {
                            //const inputField = document.querySelector(`[name="${key}"]`);
                            const inputField = document.querySelector(`#modalForm [name="${key}"]`);
                            if (inputField) {
                                inputField.value = value; // 将值填充到对应字段
                            }
                        }
                        // 特殊处理只读字段（如 ID）
                        const idField = document.querySelector('#modalForm #instanceId');
                        if (idField) idField.value = instanceId;
                    })
                    .catch(error => {
                        console.error('Error loading instance data:', error);
                    });
            }
            // 显示模态框
            modalModule.style.display = "block";
        })
        .catch(error => {
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


function generateConfirmationMessage(data) {
    let message = 'Please confirm your submission:\n\n';
    // 数据对象中的每个键值对
    for (const [key, value] of Object.entries(data)) {
        if (value) {
            // 显示键值对，并用空格代替下划线
            message += `${key.replace('_', ' ')}: ${value}\n`;
        }
        //console.log(key, value);
    }
    return message;
}


// 处理表单提交
function handleSubmit() {
    const taskMode = document.getElementById('taskMode').value;
    const objectClass = document.getElementById('titleObjectSection').textContent.toLowerCase();
    const instanceId = document.getElementById('instId').value;
    // 根据 taskMode 调用不同的函数
    if (taskMode === 'add') {
        addInstance(objectClass);
    } else if (taskMode === 'edit') {
        editInstance(objectClass, instanceId);
    } else if (taskMode === 'update') {
        editInstance(objectClass, instanceId);
    }
}


// 添加实例
function addInstance(objectClass) {
    console.log(`Adding instance of ${objectClass}`);
    // 获取表单
    const form = document.getElementById('modalForm');
    const formData = new FormData(form);  // 获取表单数据
    const jsonData = Object.fromEntries(formData.entries()); // 转换为 JSON 对象
    // 移除不必要的字段
    delete jsonData["id"];
    delete jsonData["modal_mode"];
    // 生成确认消息
    const confirmationMessage = generateConfirmationMessage(jsonData);
    // 确认提交内容
    confirmAction(confirmationMessage, function() {
        // 设置添加实例的路由
        const addUrl = `/${objectClass}/add`;
        console.log("Sending addInstance request to:", addUrl); // 检查 URL
        console.log("Form data:", jsonData); // 检查表单数据
        // 发起 AJAX 请求
        fetch(addUrl, {
            method: 'POST',
            body: JSON.stringify(jsonData),  // 确保后端可以识别这是一个 AJAX 请求
            headers: { 'Content-Type': 'application/json' }
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


// 编辑实例
function editInstance(objectClass, instanceId) {
    console.log(`Editing instance of ${objectClass} with ID ${instanceId}`);
    if (!instanceId) {
        alert("Instance ID is required for editing.");
        return;
    }
    // 获取表单
    const form = document.getElementById('modalForm');
    const formData = new FormData(form);  // 获取表单数据
    const jsonData = Object.fromEntries(formData.entries()); // 转换为 JSON 对象
    // 移除不必要的字段
    delete jsonData["modal_mode"];
    delete jsonData["inst_id"];
    // 生成确认消息
    const confirmationMessage = generateConfirmationMessage(jsonData);
    // 确认修改内容
    confirmAction(confirmationMessage, function () {
        // 设置修改实例的路由
        const editUrl = `/${objectClass}/${instanceId}/edit`;
        console.log("Sending editInstance request to:", editUrl); // 检查 URL
        console.log("Form data:", jsonData); // 检查 JSON 数据
        // 发起 AJAX 请求
        fetch(editUrl, {
            method: 'POST',
            body: JSON.stringify(jsonData),
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'  // 确保后端可以识别这是一个 AJAX 请求
            }
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            console.log("Response status:", response.status); // 检查响应状态
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data); // 检查返回数据
            if (data.success) {
                // 显示成功信息并更新页面
                alert('Instance updated successfully!');
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