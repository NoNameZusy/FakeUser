<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Block with Copy Button</title>
    <style>
        pre {
            position: relative;
            padding: 10px;
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        .copy-button {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 5px 10px;
            background-color: #333;
            color: #fff;
            border: none;
            cursor: pointer;
            font-size: 12px;
            border-radius: 4px;
        }
    </style>
</head>
<body>

<h2>FakeUser</h2>

<pre><code>apt update && apt upgrade -y</code><button class="copy-button">Copy</button></pre>

<pre><code>pip3 install -r requirements.txt</code><button class="copy-button">Copy</button></pre>

<pre><code>python3 run.py</code><button class="copy-button">Copy</button></pre>

<script>
    document.querySelectorAll('pre').forEach((codeBlock) => {
        const button = codeBlock.querySelector('.copy-button');

        button.addEventListener('click', () => {
            const code = codeBlock.querySelector('code').innerText;
            navigator.clipboard.writeText(code).then(() => {
                button.innerText = 'Copied!';
                setTimeout(() => {
                    button.innerText = 'Copy';
                }, 2000);
            });
        });
    });
</script>

</body>
</html>
