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
    // 获取模态框模块
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
            //modalModule.classList.add('is-active');
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    
    // 根据不同的 modalMode 动态赋予不同的函数给 Test 按钮
    var modalTestBtn = document.getElementById('modalTestBtn');
    if (modalMode === 'add') {
        modalTestBtn.onclick = addInstance;
    } else if (modalMode === 'edit') {
        modalTestBtn.onclick = editInstance;
    } else if (modalMode === 'update') {
        modalTestBtn.onclick = updateInstance;
    } else {
        modalTestBtn.onclick = null;
    }
}

// 确认弹窗
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}
// 删除实例
function deleteInstance(instanceId, objectClass) {
    confirmAction(`Are you sure you want to delete ${objectClass} instance ${instanceId}?`, function() {
        const deleteUrl = `/${objectClass}/${instanceId}/delete`;
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
function printInstance(instanceId, objectClass) {
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