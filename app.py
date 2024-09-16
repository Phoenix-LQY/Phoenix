from flask import Flask, render_template, request, redirect, url_for, flash
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 成员列表
members = ['朱禹霖', '王紫澄', '曾雯雯', '梁清芋']
draw_results = {}

# 查询状态
queried_members = set()
results_revealed = False

# 开发者密钥
developer_key = '.livefree'

# 首页
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        if name not in members:
            flash("同学，你名字都打错啦😒", 'error')
            return redirect(url_for('index'))

        # 记录该成员已查询
        queried_members.add(name)

        if not draw_results:  # 如果尚未抽签，进行抽签
            remaining_members = members[:]
            for member in members:
                choices = [m for m in remaining_members if m != member]
                draw_results[member] = random.choice(choices)
                remaining_members.remove(draw_results[member])

        # 成员直接跳转到其结果页面
        return redirect(url_for('result', name=name))

    # 如果结果已投送到首页，展示完整结果，否则只展示抽签按钮
    return render_template('index.html', results_revealed=results_revealed, results=draw_results, queried_members=queried_members)

# 抽签结果页面
@app.route('/result/<name>')
def result(name):
    if name in draw_results:
        chosen_member = draw_results[name]
        return render_template('result.html', name=name, chosen_member=chosen_member)
    return redirect(url_for('index'))

# 开发者页面
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        key = request.form['key']
        if key == developer_key:
            return redirect(url_for('admin_panel'))
        else:
            flash("你想干什么？🤔", 'error')
            return redirect(url_for('admin'))

    return render_template('admin.html')

# 开发者控制面板
@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    global results_revealed
    if request.method == 'POST':
        if 'reset' in request.form:
            draw_results.clear()
            queried_members.clear()
            results_revealed = False
            flash("抽签结果已重置", 'success')
        elif 'reveal' in request.form:
            results_revealed = True
            flash("结果已投送到首页", 'success')

        return redirect(url_for('admin_panel'))
 
    return render_template('admin_panel.html', results=draw_results, queried_members=queried_members)

if __name__ == '__main__':
    app.run(debug=True)
