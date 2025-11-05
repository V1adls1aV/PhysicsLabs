# М4. Физический маятник

## [Общая информация](/labs/physical_pendulum)

## Тесты

1. Свободные колебания без трения
    1. Сравнить с теор расчётом
    2. Зависимость периода от амлитуды
    3. Проверить сохранение энергии
2. Свободные колебания при наличии малого трения
    1. Сравнить с теор расчётом
    2. Проверить уменьшение общей энергии
    3. Зависимость периода колебаний от величины коеф. трения

## Теория

В качестве модели используем однородный стержень.
Распишем аналог 2-го закона Ньютона для вращательного движения  

$$
\text{угловое ускорение} \times \text{момент инерции} = \sum(\text{моментов сил})
$$

$$
I = \frac{m\,L^2}{3}\ \text{(для стержня)}
$$

### Без трения

#### Период

$$
\ddot\varphi I = -mg \frac{L}{2} \sin \varphi
$$

$$
\ddot\varphi = -mg \frac{L}{2I} \sin \varphi
$$

При малых углах (< 3..5 градусов) получим гармонические колебания

$$
\ddot\varphi + mg \frac{L}{2I} \varphi = 0
$$

Соответственно,

$$
\omega^2 = mg \frac{L}{2I}
$$

$$
T = 2\pi \sqrt{\frac{2I}{mgL}} = 2\pi \sqrt{\frac{2mL^2}{3mgL}} = 2\pi \sqrt{\frac{2L}{3g}}
$$

### С трением

Тут добавляется момент силы трения, расчитаем его далее.

$$
\ddot\varphi I = -mg \frac{L}{2} \sin \varphi + M_{\text{тр}}
$$

Расмотрим силу трения. $\beta$ – коэффициент линейного вязкого сопротивления на единицу длины стержня

$$
dF_{\text{тр}} = - \beta \omega r d r
$$

$$
dM_{\text{тр}} = - \beta \omega r^2 d r
$$

$$
dM_{\text{тр}} = - \beta \omega \int\limits_0^L r^2 d r = -\beta \dot\varphi \frac{L^3}{3}
$$

Подставим, итого:

$$
\ddot\varphi I = -mg \frac{L}{2} \sin \varphi -\beta \dot\varphi \frac{L^3}{3}
$$

При достаточно малых углах:

$$
\ddot\varphi I + \dot\varphi \beta \frac{L^3}{3} + \varphi mg \frac{L}{2}= 0
$$

$$
\ddot\varphi+ \dot\varphi \beta \frac{L}{m} + \varphi \frac{3g}{2L} = 0
$$

#### Найдем решения

$$2\gamma\omega_0=\beta \frac{L}{m}$$

$$\omega_0^2=\frac{3g}{2L},\quad\omega_0=\sqrt{\tfrac{3g}{2L}}$$

$$\gamma=\dfrac{\beta L}{2m\omega_0}=\dfrac{\beta L}{2m}\sqrt{\tfrac{2L}{3g}}$$


Тогда уравнение имеет вид:

$$\ddot\varphi+2\gamma\omega_0\dot\varphi+\omega_0^2\varphi=0$$

Характеристическое уравнение:

$$r^2+( \beta L/m)\,r+3g/(2L)=0$$

#### Формулы решений

1. Экспоненциальное затухание без единого колебания $(\gamma \ge 1)$: $$\varphi(t)=C_1 e^{r_1 t}+C_2 e^{r_2 t},\quad r_{1,2} < 0$$

2. Экспоненциальное затухание амплитуды с периодическими колебаниями $(\gamma<1)$:

$$\varphi(t)=e^{-\gamma\omega_0 t}\left(C_1\cos(\omega_d t)+C_2\sin(\omega_d t)\right)$$
$$\omega_d=\omega_0\sqrt{1-\gamma^2}$$

Функции расчета этих теор решений можно найти в
[calculations.py](/tests/physical_pendulum/calculations.py)

### Энергия

Энергия вычисляется идентично в обоих случаях.

$E_{\text{п}}=mg\,\frac{L}{2}\,(1-\cos\varphi)$

$E_{\text{вр}} = \frac{I\,\dot\varphi^{2}}{2}$

Часть тестов направлена на проверку сохранения полной энергии при колебаниях без трения и на спад общей энергии при наличии трения.
