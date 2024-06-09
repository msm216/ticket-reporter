from app import create_app

# 通过 __init__.py 中的 create_app() 函数创建app
app = create_app()

if __name__ == '__main__':
    
    app.run(debug=True)