Let $x(t)$ be the position of the autonomous arm at time $t$, and let $y$ be the target position. We define the Euclidean distance between $x(t)$ and $y$ as:

$$D_E(x(t),y)=\sqrt{\sum_{i=1}^n(y_i-x_i(t))^2}$$

We also define the Chebyshev distance as:

$$D_C(x(t),y)=\max_{i=1}^n|x_i(t)-y_i|$$

And the Minkowski distance with parameter $p_1$ as:

$$D_M(x(t),y,p_1)=\left(\sum_{i=1}^n|x_i(t)-y_i|^{p_1}\right)^{\frac{1}{p_1}}$$

We now define a new distance metric:

$$D(x(t),y,p)=\max\{D_C(x(t),y), D_M(x(t),y,p_2)\}$$

where $p = \max{p_1, p_2}$ and $p_2$ is the parameter for the Minkowski distance that depends on the current and previous Euclidean distances to the target, as defined in the problem statement.

We want to show that $D(x(t), y, p)$ converges faster than $D_E(x(t), y)$ in an environment with obstacles.

To do this, we first note that $D(x(t), y, p)$ is always greater than or equal to $D_E(x(t), y)$, since both $D_C(x(t), y)$ and $D_M(x(t), y, p_2)$ are non-negative. Therefore, we only need to show that $D(x(t), y, p)$ converges faster than $D_E(x(t), y)$.

Let $d_E(t) = D_E(x(t), y)$ be the Euclidean distance at time $t$. We want to compare the rate of convergence of $D(x(t), y, p)$ to $d_E(t)$. We can do this by comparing the rates of change of $D_C(x(t), y)$ and $D_M(x(t), y, p_2)$ to the rate of change of $d_E(t)$.

Taking the derivative of $d_E(t)$ with respect to time $t$, we get:

$$\frac{d}{dt} d_E(t) = -\frac{d_E(t)}{dx}\cdot\sum\limits_{i=1}^n (y_i - x_i(t))\cdot \frac{d}{dt}x_i$$

Taking the derivative of $D_C(x(t), y)$ with respect to time $t$, we get:

$$\frac{d}{dt} D_C(x(t), y) = \max\limits_{i=1}^n \operatorname{sgn}(x_i(t) - y_i) \cdot \frac{d}{dt} x_i$$

where $\operatorname{sgn}(x_i(t) - y_i)$ is the sign of the difference between the $i$th component of $x(t)$ and $y$. Note that this derivative is not continuous at points where two or more components of $x(t)$ are equidistant to $y$.

Taking the derivative of $D_M(x(t), y, p_2)$ with respect to time $t$, we get:

$$\frac{d}{dt} D_M(x(t),y,p_2) = p_2^{1-p_2} \cdot \sum\limits_{i=1}^n \text{sgn}(x_i(t)-y_i) \cdot \vert x_i(t)-y_i \vert^{p_2-1} \cdot \frac{d x_i(t)}{dt}$$

where $\operatorname{sgn}(x_i(t) - y_i)$ is the sign of the difference between the $i$th component of $x(t)$ and $y$.

Now, we can use the fact that $p_2 = ||y - x(t)||_2 - ||y - x(t-1)||_2$ to rewrite the derivative of $D_M(x(t), y, p_2)$ as:

$$\frac{d}{dt} D^M(x(t),y,p_2) = \frac{p_2}{1} \sum_{i=1}^n \operatorname{sgn}(x_i(t)-y_i) \cdot \left|x_i(t)-y_i\right|^{p_2-1} \cdot \left(\left|y-x(t-1)\right|^2 - \left|y-x(t)\right|^2\right)$$

Now, we can compare the rates of change of $D_C(x(t), y)$ and $D_M(x(t), y, p_2)$ to the rate of change of $d_E(t)$ by taking their absolute values:

$$\begin{equation*}
\left\lvert\frac{d}{dt} D_C(x(t),y)\right\rvert = \max_{i=1}^n \left\lvert sgn(x_i(t)-y_i) \cdot \frac{dt}{dx_i}\right\rvert \leq \left\lvert\frac{d}{dt} D_E(t)\right\rvert
\end{equation*}$$

$$\left|\left|\frac{d}{dt} D_M(x(t), y, p_2)\right|\right| = \frac{1}{p_2}\cdot$$

Since $p_2$ is positive and $|x_i(t) - y_i|^{p_2-1}$ is non-negative, we have:

$$\begin{equation*}
\left\vert\frac{d}{dt}D_{M}(x(t), y, p_2)\right\vert \geq \left|\left|y-x(t-1)\right|^2-\left|y-x(t)\right|^2\right|\cdot\left|\left|\frac{d}{dt}E(t)\right|\right|\end{equation*}$$


Therefore, we see that the rate of change of $D_M(x(t), y, p_2)$ is at least as large as the rate of change of $d_E(t)$ times the absolute difference between $||y - x(t-1)||_2$ and $||y - x(t)||_2$. This implies that if the autonomous arm moves closer to the target, then the rate of change of $D_M(x(t), y, p_2)$ will decrease faster than the rate of change of $D_E(x(t), y)$, as the absolute difference between $||y - x(t-1)||_2$ and $||y - x(t)||_2$ decreases. Thus, we can expect that the autonomous arm will converge to the target faster using the Minkowski distance with $p_2$ than using the Euclidean distance.

Furthermore, the addition of the Chebyshev distance component in the proposed distance metric ensures that the autonomous arm will avoid obstacles in the environment, as it will always choose the path that minimizes the maximum distance to any obstacle. Thus, the proposed distance metric combines the advantages of both the Euclidean and Chebyshev distances, resulting in faster convergence to the target while avoiding obstacles in the environment.

Therefore, we conclude that the proposed distance metric, which is a combination of the Minkowski distance with $p_2$ and the Chebyshev distance, converges faster than the Euclidean distance metric in an environment with obstacles.
