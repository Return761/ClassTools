document.addEventListener("DOMContentLoaded", function () {
    // 1. 初始化 WebChannel
    new QWebChannel(qt.webChannelTransport, function (channel) {
        // 获取 Python 中注册的 "pyObj" 对象
        window.pyObj = channel.objects.pyObj;

        // --- 监听 Python 主动发来的信号 ---
        pyObj.on_status_update.connect(function (message) {
            document.getElementById("clock").innerText = message;
        });

        console.log("WebChannel 连接成功！");
    });

    // 2. 绑定按钮点击事件
    document.getElementById("btn").onclick = async function () {
        const resEl = document.getElementById("result");
        resEl.innerText = "Python 正在计算中...";

        // --- 异步调用 Python 的 Slot ---
        // 在 JS 中，调用是异步的，直接使用 await 获取返回值
        const result = await pyObj.heavy_task("数据");
        resEl.innerText = result;
    };
});