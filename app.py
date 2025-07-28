from flask import Flask, request, render_template
import math


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    roots = None
    error = None

    if request.method == 'POST':
        try:
            a = float(request.form.get('a'))
            b = float(request.form.get('b'))
            c = float(request.form.get('c'))

            if a == 0:
                error = 'Коэффициент a не должен быть нулём'
            else:
                d = b ** 2 - 4 * a * c
                result = f'D = {d}'

                if d > 0:
                    x1 = (-b + math.sqrt(d)) / (2 * a)
                    x2 = (-b - math.sqrt(d)) / (2 * a)
                    roots = (
                        f'x₁ = {x1:.3f}, '
                        f'x₂ = {x2:.3f}'
                    )
                elif d == 0:
                    x = -b / (2 * a)
                    roots = f'x = {x:.3f}'
                else:
                    roots = 'Корней нет (D < 0)'

        except Exception as e:
            error = f'Ошибка: {str(e)}'

    return render_template(
        'index.html',
        result=result,
        roots=roots,
        error=error
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
