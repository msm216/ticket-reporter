// 提交模态框表单
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