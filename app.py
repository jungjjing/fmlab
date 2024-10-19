from flask import Flask, request, session, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션에 사용될 비밀 키 설정

@app.route('/')
def index():
    # 첫 페이지로 splash.html 렌더링
    return render_template('splash.html')

@app.route('/start_1', methods=['GET', 'POST'])
def start_1():
    if request.method == 'POST':
        # start_1.html에서 버튼을 누르면 start_2로 리다이렉트
        return redirect('/start_2')
    # 처음 로드될 때 start_1.html 렌더링
    return render_template('start_1.html')

@app.route('/start_2', methods=['GET', 'POST'])
def start_2():
    if request.method == 'POST':
        # start_2.html에서 버튼을 누르면 start_3로 리다이렉트
        return redirect('/start_3')
    # 처음 로드될 때 start_2.html 렌더링
    return render_template('start_2.html')

@app.route('/start_3', methods=['GET', 'POST'])
def start_3():
    if request.method == 'POST':
        # 사용자가 입력한 이름을 세션에 저장
        session['username'] = request.form.get('username')
        # 다음 페이지로 리다이렉트
        return redirect('/start_4')
    return render_template('start_3.html')

@app.route('/start_4')
def start_4():
    username = session.get('username', '사용자')
    # 3초 후 자동으로 /question1으로 넘어가게 설정된 페이지 렌더링
    return render_template('start_4.html', username=username)



@app.route('/question1', methods=['GET', 'POST'])
def question1():
    if request.method == 'POST':
        session['question1'] = {
            'choice': request.form.get('choice'),
            'label': request.form.get('label')
        }
        return redirect('/question2')
    return render_template('test_1.html')

@app.route('/question2', methods=['GET', 'POST'])
def question2():
    if request.method == 'POST':
        session['question2'] = {
            'choice': request.form.get('choice'),
            'label': request.form.get('label')
        }
        return redirect('/question3')
    return render_template('test_2.html')

@app.route('/question3', methods=['GET', 'POST'])
def question3():
    if request.method == 'POST':
        session['question3'] = {
            'choice': request.form.get('choice'),
            'label': request.form.get('label')
        }
        return redirect('/question4')
    return render_template('test_3.html')

@app.route('/question4', methods=['GET', 'POST'])
def question4():
    if request.method == 'POST':
        session['question4'] = {
            'choice': request.form.get('choice'),
            'label': request.form.get('label')
        }
        return redirect('/question5')
    return render_template('test_4.html')

@app.route('/question5', methods=['GET', 'POST'])
def question5():
    if request.method == 'POST':
        session['question5'] = {
            'choice': request.form.get('choice'),
            'label': request.form.get('label')
        }
        # 설문이 끝난 후 동점 여부를 확인
        return redirect('/check_tiebreaker')
    return render_template('test_5.html')

@app.route('/check_tiebreaker')
def check_tiebreaker():
    # 각 라벨의 선택 횟수를 계산
    label_counts = {'curious': 0, 'lively': 0, 'nervous': 0, 'ord': 0, 'trust': 0}

    # 세션에서 모든 질문의 결과를 가져와 라벨별로 집계
    for i in range(1, 6):
        question = session.get(f'question{i}')
        if question and 'label' in question:
            label = question['label']
            if label in label_counts:
                label_counts[label] += 1

    # 동점 여부 확인
    max_count = max(label_counts.values())
    top_labels = [label for label, count in label_counts.items() if count == max_count]

    # 동점인 경우에 따라 11가지 중 하나의 경우로 분기
    if len(top_labels) > 1:
        top_labels.sort()
        label_key = '-'.join(top_labels)
        # 11가지 동점의 경우에 따라 다른 추가 설문 페이지로 이동
        if label_key == 'curious-lively':
            return redirect('/tiebreaker_test_6_1')
        elif label_key == 'curious-ord':
            return redirect('/tiebreaker_test_6_2')
        elif label_key == 'curious-trust':
            return redirect('/tiebreaker_test_6_3')
        elif label_key == 'curious-nervous':
            return redirect('/tiebreaker_test_6_4')
        elif label_key == 'lively-ord':
            return redirect('/tiebreaker_test_6_5')
        elif label_key == 'lively-trust':
            return redirect('/tiebreaker_test_6_6')
        elif label_key == 'lively-nervous':
            return redirect('/tiebreaker_test_6_7')
        elif label_key == 'ord-trust':
            return redirect('/tiebreaker_test_6_8')
        elif label_key == 'ord-nervous':
            return redirect('/tiebreaker_test_6_9')
        elif label_key == 'trust-nervous':
            return redirect('/tiebreaker_test_6_10')
        elif label_key == 'curious-lively-nervous-ord-trust':
            return redirect('/tiebreaker_test_6_11')
    else:
        # 1등 라벨이 명확한 경우 바로 결과 페이지로 이동
        return redirect('/result')

# 11가지 동점 패턴에 따른 추가 설문 페이지
@app.route('/tiebreaker_test_6_1', methods=['GET', 'POST'])
def tiebreaker_test_6_1():
    return handle_tiebreaker('test_6_1.html')

@app.route('/tiebreaker_test_6_2', methods=['GET', 'POST'])
def tiebreaker_test_6_2():
    return handle_tiebreaker('test_6_2.html')

@app.route('/tiebreaker_test_6_3', methods=['GET', 'POST'])
def tiebreaker_test_6_3():
    return handle_tiebreaker('test_6_3.html')

@app.route('/tiebreaker_test_6_4', methods=['GET', 'POST'])
def tiebreaker_test_6_4():
    return handle_tiebreaker('test_6_4.html')

@app.route('/tiebreaker_test_6_5', methods=['GET', 'POST'])
def tiebreaker_test_6_5():
    return handle_tiebreaker('test_6_5.html')

@app.route('/tiebreaker_test_6_6', methods=['GET', 'POST'])
def tiebreaker_test_6_6():
    return handle_tiebreaker('test_6_6.html')

@app.route('/tiebreaker_test_6_7', methods=['GET', 'POST'])
def tiebreaker_test_6_7():
    return handle_tiebreaker('test_6_7.html')

@app.route('/tiebreaker_test_6_8', methods=['GET', 'POST'])
def tiebreaker_test_6_8():
    return handle_tiebreaker('test_6_8.html')

@app.route('/tiebreaker_test_6_9', methods=['GET', 'POST'])
def tiebreaker_test_6_9():
    return handle_tiebreaker('test_6_9.html')

@app.route('/tiebreaker_test_6_10', methods=['GET', 'POST'])
def tiebreaker_test_6_10():
    return handle_tiebreaker('test_6_10.html')

@app.route('/tiebreaker_test_6_11', methods=['GET', 'POST'])
def tiebreaker_test_6_11():
    return handle_tiebreaker('test_6_11.html')

def handle_tiebreaker(template_name):
    if request.method == 'POST':
        # 추가 설문의 결과를 세션에 저장
        tiebreaker_choice = request.form.get('tiebreaker_choice')
        session['tiebreaker_result'] = tiebreaker_choice
        return redirect('/result')
    # 추가 설문 페이지 렌더링
    return render_template(template_name)

@app.route('/show_load1/<result_page>')
def show_load1(result_page):
    # 5초 동안 load1.html 표시
    return render_template('load1.html', next_page=url_for('show_load2', result_page=result_page))

@app.route('/show_load2/<result_page>')
def show_load2(result_page):
    # 3초 동안 load2.html 표시
    return render_template('load2.html', next_page=url_for(result_page))

@app.route('/result')
def result():
    # 각 라벨의 선택 횟수를 계산
    label_counts = {'curious': 0, 'lively': 0, 'nervous': 0, 'ord': 0, 'trust': 0}

    # 세션에서 모든 질문의 결과를 가져와 라벨별로 집계
    for i in range(1, 6):
        question = session.get(f'question{i}')
        if question and 'label' in question:
            label = question['label']
            if label in label_counts:
                label_counts[label] += 1

    # 추가 설문의 결과를 반영
    if 'tiebreaker_result' in session:
        label_counts[session['tiebreaker_result']] += 1

    # 1등 라벨을 판별
    top_label = max(label_counts, key=label_counts.get)
    username = session.get('username', '사용자')

    # 1등 라벨에 따라 중간 로드 페이지로 리다이렉트하여 최종 서브페이지로 이동
    if top_label == 'curious':
        return redirect(url_for('show_load1', result_page='curious_result'))
    elif top_label == 'lively':
        return redirect(url_for('show_load1', result_page='lively_result'))
    elif top_label == 'nervous':
        return redirect(url_for('show_load1', result_page='nervous_result'))
    elif top_label == 'ord':
        return redirect(url_for('show_load1', result_page='ord_result'))
    elif top_label == 'trust':
        return redirect(url_for('show_load1', result_page='trust_result'))
    else:
        return "Unexpected error: No valid label found."

# 각 라벨에 해당하는 서브페이지 라우트 설정
@app.route('/curious_result')
def curious_result():
    username = session.get('username', '사용자')
    return render_template('c_result1.html', username=username)

@app.route('/lively_result')
def lively_result():
    username = session.get('username', '사용자')
    return render_template('l_result1.html', username=username)

@app.route('/nervous_result')
def nervous_result():
    username = session.get('username', '사용자')
    return render_template('n_result1.html', username=username)

@app.route('/ord_result')
def ord_result():
    username = session.get('username', '사용자')
    return render_template('o_result1.html', username=username)

@app.route('/trust_result')
def trust_result():
    username = session.get('username', '사용자')
    return render_template('t_result1.html', username=username)

# 새로운 t_result2 라우트 추가
@app.route('/t_result2')
def t_result2():
    username = session.get('username', '사용자')
    return render_template('t_result2.html', username=username)

@app.route('/t_result3')
def t_result3():
    return render_template('t_result3.html')

@app.route('/t_result1')
def t_result1():
    # 세션에서 username을 가져옵니다. 만약 없다면 '사용자'로 기본값을 설정합니다.
    username = session.get('username', '사용자')
    return render_template('t_result1.html', username=username)


@app.route('/c_result2')
def c_result2():
    username = session.get('username', '사용자')
    return render_template('c_result2.html', username=username)

@app.route('/c_result3')
def c_result3():
    return render_template('c_result3.html')

@app.route('/c_result1')
def c_result1():
    # 세션에서 username을 가져옵니다. 만약 없다면 '사용자'로 기본값을 설정합니다.
    username = session.get('username', '사용자')
    return render_template('c_result1.html', username=username)

@app.route('/n_result2')
def n_result2():
    username = session.get('username', '사용자')
    return render_template('n_result2.html', username=username)

@app.route('/n_result3')
def n_result3():
    return render_template('n_result3.html')

@app.route('/n_result1')
def n_result1():
    # 세션에서 username을 가져옵니다. 만약 없다면 '사용자'로 기본값을 설정합니다.
    username = session.get('username', '사용자')
    return render_template('n_result1.html', username=username)
    
@app.route('/l_result2')
def l_result2():
    username = session.get('username', '사용자')
    return render_template('l_result2.html', username=username)

@app.route('/l_result3')
def l_result3():
    return render_template('l_result3.html')

@app.route('/l_result1')
def l_result1():
    # 세션에서 username을 가져옵니다. 만약 없다면 '사용자'로 기본값을 설정합니다.
    username = session.get('username', '사용자')
    return render_template('l_result1.html', username=username)

@app.route('/o_result2')
def o_result2():
    username = session.get('username', '사용자')
    return render_template('o_result2.html', username=username)

@app.route('/o_result3')
def o_result3():
    return render_template('o_result3.html')

@app.route('/o_result1')
def o_result1():
    # 세션에서 username을 가져옵니다. 만약 없다면 '사용자'로 기본값을 설정합니다.
    username = session.get('username', '사용자')
    return render_template('o_result1.html', username=username)

if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0')
