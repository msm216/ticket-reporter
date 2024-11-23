// 提交模态框表单 留档
function submitIssue() {
    var id = document.getElementById('issueId').value;
    var name = document.getElementById('userName').value || '';
    var group_id_str = document.getElementById('userGroupID').value || 0;
    // Ensure group_id is an integer
    var group_id = parseInt(group_id_str, 10);
    if (isNaN(group_id)) {
        group_id = 0; // or any other default value
    }
    // 如果获取 'userRegisteredOn' 的为空值（包括''）则以当天日期赋值
    var registered_on = document.getElementById('userRegisteredOn').value || new Date().toISOString().split('T')[0];
    var mode = document.getElementById('userModalMode').value;
    // 根据 mode 条件赋值 url
    var url
    switch (mode) {
        case 'add':
            url = '/add_user';
            break;
        case 'edit':
            url = '/edit_user/' + id;
            break;
        default:
            // 未知模式直接返回
            console.error('Unknown mode:', mode);
            return;
    }
    ////////////////
    console.log('Submitting User:')
    console.log('id: ', id)
    console.log('name: ', name)
    console.log('registered_on:', registered_on, 'of type: ', typeof registered_on);
    console.log('group_id:', group_id, 'of type: ', typeof created_on);
    console.log('mode: ', mode)
    ////////////////
    var data = {
        name: name,
        registered_on: registered_on,
        group_id: group_id
    };
    confirmAction('Are you sure you want to ' + (mode === 'add' ? 'add this instance?' : 'modify this instance?'), function() {
        // 发送请求
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.message);
            }
        });
    });
}


// 开启模态框 留档
function openModal(objectClass, instanceId, modalMode) {
    // 获取模态框模块
    const moodalID = `${objectClass}${capitalizeFirstLetter(modalMode)}Modal`;
    console.log("Dynamic modal ID: ", moodalID);
    const modalModule = document.getElementById('modalModule');
    // 设置标题
    document.getElementById('titleActionSection').textContent = modalMode ? capitalizeFirstLetter(modalMode) : 'Action';
    document.getElementById('titleObjectSection').textContent = objectClass ? capitalizeFirstLetter(objectClass) : 'Object';
    document.getElementById('titleIdSection').textContent = instanceId ? ` ${instanceId}` : '';
    // 设置隐藏字段
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
            //var modalForm = modalModule.querySelector('.modal-form');
            //modalForm.action = instanceId ? `/${objectClass}/${instanceId}/${modalMode}` : `/${objectClass}/${modalMode}`;
            //console.log("Form action URL: ", modalForm.action);
            // 绑定Submit按钮的点击事件，根据 modalMode 调用不同函数
            var modalSubmitBtn = document.getElementById('modalSubmitBtn');
            modalSubmitBtn.onclick = () => {
                if (modalMode === 'add') {
                    addInstance(objectClass);
                } else if (modalMode === 'edit') {
                    editInstance(objectClass, instanceId);
                }
            };
            // 显示模态框
            modalModule.style.display = "block";
        })
        .catch(error => {
            console.error('Error loading form:', error);
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
