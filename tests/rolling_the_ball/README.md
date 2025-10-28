# М4. Шар на столе

## [Общая информация](/labs/rolling_the_ball)

## Тесты

1. $t_s$ – сравнение с аналитическим решением (и скоростей)
2. На плоскости ($\alpha = 0$)
3. Корректность (проверка утверждений ниже: 1, 2, 3)
4. Примеров, полность состоящих из движения с/без проскальзования

## Вывод формул и проверка корректности алгоритма

### Вращательное движение

$$
\frac{dL}{dt}=M
$$
$$
I = \frac{2}{5} m R^2 \quad \text{(шар)}
$$
$$
I \frac{d \omega}{dt} = F_{\text{тр}}R
$$
$$
\dot \omega = \frac{\mu mgR \cos \alpha}{I}
$$
$$
\omega (t) = \frac{\mu mgR \cos \alpha}{I} t
$$

### Поступательное движение

$$
\sum\limits \vec F = m \vec a
$$
$$
\vec F_{\text{тр}}+\vec N + m \vec g = m \vec a
$$
$$
Рассмотрим\ Ox : -F_{\text{тр}} + m g \sin \alpha = m \frac{d\upsilon}{dt}
$$
$$F_{тр}=\mu N = \mu mg \cos \alpha$$
$$
\dot\upsilon = g(\sin \alpha - \mu \cos \alpha)
$$
$$
\upsilon(t) = \upsilon_0 + gt(\sin \alpha - \mu \cos \alpha)
$$

### Случай с проскальзованием

$$

\begin{cases}

\omega (t) = \frac{\mu mgR \cos \alpha}{I} t \\

\upsilon (t) = \upsilon_0 + (\sin \alpha - \mu \cos \alpha)gt \\

\end{cases}

$$

$$
t_{s} = \frac{\upsilon_{0}}{\frac{1}{I}\mu mgR^{2} \cos \alpha + (\mu \cos \alpha - \sin \alpha )g}
$$
$$
t_{s} = \frac{\upsilon_{0}}{g(\frac{2}{7} \mu  \cos \alpha + - \sin \alpha)}
$$

### Случай без проскальзования
$\upsilon = \omega R, \ \dot\upsilon = \dot\omega R$

$$
I \dot{\omega} = F_{\text{тр}} R
$$

$$
F_{\text{тр}} = \frac{I \dot{\omega}}{R}
$$

$$
F_{\text{тр}} = \frac{I \dot{\upsilon}}{R^2}
$$

$$
m \dot{\upsilon} + \frac{I \dot{\upsilon}}{R^2} = mg \sin \alpha
$$

$$
\dot{\upsilon} = \frac{mg \sin \alpha}{m + \frac{I}{R^2}}
$$

### Проверим теорию для тестов

#### 1. Если $\alpha = 0$, то шар двигается равномерно и прямолинейно в фазе без проскальзования

Подставим в $\dot\upsilon$ (из движения во второй фазе) $\alpha = 0$. Получим $\dot\upsilon = 0$, то есть ускорение равно нулю.

#### 2. Если $\mu = 0$, то шар двигается только поступательно.

$F_{\text{тр}} = 0$, то есть $mg$ не может развернуть шар из-за отсутсвия взаимодействия шара и склона по касательной.

Подставим в $\omega(t) \ \mu=0$, получим $\omega(t) = 0$.

#### 3. Скорость возрастания $\omega$ становится строго меньше при переходе к фазе без проскальзования ($\dot\omega_1 > \dot\omega_2$)

$$
\dot{\omega} = \frac{F_{\text{тр}} R}{I}
$$

$$
\dot\omega_1 \; ? \ \dot\omega_2
$$

$$
F_{\text{тр1}} \; ? \ F_{\text{тр2}}
$$

Получим $F_{\text{тр2}}$:

$$
F_{\text{тр2}} = \frac{\dot{\omega} I}{R} = \frac{I \dot{v}}{R^2}
$$

$$
F_{\text{тр2}} = \frac{2}{5} m \dot{v}
$$

Сравним:

$$
\mu mg \cos \alpha \; ? \ \frac{2}{5} m \dot{v}
$$

$$
\mu g \cos \alpha \; ? \ \frac{2}{5} \dot{v}
$$


$$
\dot{v} = \frac{5g \sin \alpha}{7}
$$

$$
\mu \cos d \; ? \ \frac{2}{7} \sin \alpha
$$

$$
\mu \; ? \ \frac{2}{7} \; \tg \alpha
$$

Однако, из предположения $t_{s} > 0$ и $\upsilon_0 > 0$ следует "знаменатель" > 0. $\Rightarrow (\mu > \frac{2}{7} \tg \alpha)$

Получаем: $\dot\omega_1 > \dot\omega_2 \quad \blacksquare$
