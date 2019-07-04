var TableString = ` <tr>
<th>姓名</th><td>name</td>
<th>性别</th><td>sex</td>
</tr>
<tr>
<th>学号</th><td>id</td>
<th>住址</th><td>address</td>
</tr>
<tr>
<th>电话</th><td>phone</td>
<th>出生年月</th><td>birthday</td>
</tr>
<tr>
<th>籍贯</th><td>{%county%}</td>
<th>学科</th><td>dept</td>
</tr>
<tr>
<th>班级</th><td>{%class%}</td>
<th></th><td></td>
</tr>`
var TS = ''
$(function () {
    try {
        cookieContent = get_cookie('WTF');
        if (cookieContent == undefined) {
            alert('请先去登录')
            window.location.href = '/'
        }
        cookieContent = cookieContent.replace('[', '').replace(']', '').replace(/"/g, '').split(',');
        studentName = $.trim(cookieContent[1]);
        studentId = $.trim(cookieContent[0])
        document.getElementsByClassName('WelCome')[0].innerHTML = '欢迎' + studentName + '同学登录';
        showinfo(studentId)
    } catch {
        window.location.href = '/';
    }
})

function showinfo(id) {
    $.ajax({
        url: '/QstudentQuery',
        type: 'POST',
        data: {
            studentId: id,
        },
        dataType: 'json',
        success: function (data) {
            console.log(data)
            let name = data[0][0];
            let id = data[0][1];
            let address = data[0][2];
            let sex = data[0][3];
            let phone = data[0][4];
            let birthday = data[0][5];
            let country = data[0][6];
            let dept = data[0][7];
            let classs = data[0][8];
        
            TS += TableString.replace('name', name).replace('id', id)
            .replace('address', address).replace('sex', sex).replace('phone', phone)
            .replace('birthday', birthday).replace('{%county%}', country).replace('dept', dept)
            .replace('{%class%}', classs)
            console.log(TS)
             $('.card-block table').append(TS);
        },
        error: function (err) {
            console.log(err)
        }
    })
}