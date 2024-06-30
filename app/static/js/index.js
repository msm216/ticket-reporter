// 生成对应的初始化函数名称。例如：如果 page 是 'about'，则生成 'updateAboutPage'
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// 调用 loadContent('about') 时：
// -- fetch('/about') 发送请求获取 about.html 的内容。
// -- 响应的 HTML 被插入到 id="content" 的 <div> 中。
// -- 动态加载 static/js/about.js 文件。
// -- 当 about.js 加载完成后，调用 updateAboutPage() 函数（如果存在）。
function loadContent(page) {
    // fetch 是一个现代的异步 API，用于从服务器获取资源。在这里，它通过路径 /${page} 发送一个请求
    fetch(`/${page}`)
        // 处理 fetch 的响应，将其转换为文本。因为我们期望从服务器获取的是 HTML 文本内容
        .then(response => response.text())
        // 当上一步成功获取到 HTML 文本时，执行回调函数
        .then(html => {
            // 获取页面中 ID 为 content 的 <div> 元素
            const contentDiv = document.getElementById('content');
            // 将获取到的 HTML 内容插入到 contentDiv 中。这会更新页面显示的内容
            contentDiv.innerHTML = html;
            // 动态创建一个 <script> 元素来加载对应的 JavaScript 文件
            const script = document.createElement('script');
            // 设置 <script> 元素的 src 属性为需要相应加载的脚本路径
            script.src = `static/js/${page}.js`;
            // 设置一个事件处理器，当 <script> 文件加载完成时执行
            script.onload = () => {
                // 调用对应的初始化函数
                //const initFunctionName = `update${capitalizeFirstLetter(page)}Page`;
                // 检查是否存在这个初始化函数，并在存在时调用它。这确保了每个页面加载后，能够执行其特定的初始化逻辑
                if (typeof window[`update${capitalizeFirstLetter(page)}Page`] === 'function') {
                    window[`update${capitalizeFirstLetter(page)}Page`]();
                }
            };
            // 将 <script> 元素添加到页面的 <body> 中。这会触发浏览器加载并执行这个脚本文件
            document.body.appendChild(script);
        })
        .catch(error => console.error('Error loading content:', error));
}

// Function to switch navigation sections
function switchNav(navId) {
    document.querySelectorAll('.nav').forEach(nav => {
        nav.style.display = 'none';
    });
    document.getElementById(navId).style.display = 'block';
}