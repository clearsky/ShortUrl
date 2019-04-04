# ShortUrl
setshorturl接口:
1. 接口地址:/setshorturl/
2. 请求方式:POST
3. 请求参数：

名称 | 必填 | 类型  | 说明 |
-|-|-|-
long_url | 是 | string | 用户要转换的长链接 |
short_url | 否 | string | 用户自定义的短链接key |
qrcode | 否 | 不限 | 只要传如此参数，就返回短链接的二维码 |
4. 返回参数说明

名称 | 类型  | 说明 |
-|-|-
msg | string | 正常情况为ok，出错返回错误描述
short_url | string | 生成的短链接
long_url | string | 用户传入的长链接
code | int | 正常为0，出错返回错误状态码
qrcode | string 或者 bool | 如果用户请求了二维码，返回base64编码的字符流的str数据，否则返回False

5.json返回示例
```json
{
	"msg": "ok",
	"short_url": "http://127.0.0.1:8000/sssddd",
	"long_url": "http://www.baidu.com/fdsafa",
	"code": 0,
	"qrcode": "iVBORw0KGgoAAAANSUhEUgAAAXIAAAFyAQAAAADAX2ykAAACeElEQVR4nO2aTYrcMBBGX8WGXsowB8hR7BvMkYbczD5K30BaDqipLKTydNwJkyYex4LSQt1Yb/FBUb+SKM+s5dtTODjvvPPOO++883/ipa4eFhERGUAmbgLJzqYD9Ti/Mz+qqmoEmUJG9SoCgEx0qqqqv/Jfrcf5nflUPVQ1dsoydMWgOgPFsY/V4/w+fP/wJb1kgZso6eWxeTqbfuef40WGmxQnJrxb1v1/epz/N978NyiQoHjs8prLZ/34dowe5/fluS+e6JQxbjY7G1VV57Ppd/6TpZs1h4zOWH21PT2bfuf/hpcp9WWD1CNv8SY6h+rYUjrhA/U4vxdf8q+SbgIhA3QZEkDqM8sEugxRZZyP0OP8vnyxrxByr6QBJURYXmtKFkJExqu57+n0O//JKvVVqaU0rwk3l9FG3YIdeP5tjDe70WnpelcjQ6gzS51D9vq5ZV7eIoh8z7DIRVmGtaACIF18/twmf9f/1qlV+UdxWMbYlXDt/tskfxeLGYsZSxGtEDK1SfL82ypvBVXs1KYadWqlc7AD999m+bv7IyFEtF4d2cdlotwkyTF6nN+Xt/5I85p/OyudVdcg7f7bKL/2R9y3vqX/tUm097/t8nf+a6vTUjrXcSX2esft2yxf5xulIQL9Ufrf1dLJ39c1ym/vf2t8jtROaYy1U/L82zJfInAEwN7XLQN8BGmdj9Tj/M68RWARsftfvV6URUR+x3+1Huf34bfvJ5U0iFbXfRcIEcGec5xPv/PP8TKV3xqka1ROvR2cXb/zm2X90ccs0m4F1/mGz5/b5R/fT5qJa2uE188t8/b+ytbm37p5/nXeeeedd975/fifTngQs3CHdjIAAAAASUVORK5CYII="
}
```
