def cal_pai_mc(n=1000000):
 r = 1.0
 a, b = (0.0, 0.0)
 x_neg, x_pos = a - r, a + r
 y_neg, y_pos = b - r, b + r
 m = 0
 for i in range(0, n+1):
 x = random.uniform(x_neg, x_pos)
 y = random.uniform(y_neg, y_pos)
 if x**2 + y**2 <= 1.0:
 m += 1
 return (m / float(n)) * 4

2.计算函数定积分值
实验原理：若要求函数f(x)从a到b的定积分，我们可以用一个比较容易算得面积的矩型包围在函数的积分区间上（假设其面积为Area），定积分值其实就是求曲线下方的面积。随机地向这个矩形框里面投点，统计落在函数f(x)下方的点数量占所有点数量的比例为P，那么就可以据此估算出函数f(x)从a到b的定积分为Area×P。此处我们将a和b设为0和1，函数f(x)=x2。
运行结果为0.333749


def cal_integral_mc(n = 1000000):
 x_min, x_max = 0.0, 1.0
 y_min, y_max = 0.0, 1.0
 m = 0
 for i in range(0, n+1):
 x = random.uniform(x_min, x_max)
 y = random.uniform(y_min, y_max)
 # x*x > y 表示该点位于曲线的下面。
 if x*x > y:
 m += 1
 #所求的积分值即为曲线下方的面积与正方形面积的比
 return m / float(n)
