var TableString = `<tr class="pass">
<td>{%Tid%}</td>
<td>{%Cname%}</td>
<td>{%credit%}</td>
<td>{%Tname%}</td>
</tr>`;
var TS = '';
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
        var years = document.getElementById('years');
        var index = years.selectedIndex;
        var yearsValue = years.options[index].value;
        var sa = document.getElementById('springAndautumn');
        var saindex = sa.selectedIndex;
        var saValue = sa.options[saindex].value;
        showtable(studentId, yearsValue, saValue)
    } catch {
        window.location.href = '/';
    }
})

function chaxun() {
    $('.card-block table').append('');
    var years = document.getElementById('years');
    var index = years.selectedIndex;
    var yearsValue = years.options[index].value;
    var sa = document.getElementById('springAndautumn');
    var saindex = sa.selectedIndex;
    var saValue = sa.options[saindex].value;
    $('.card-block table td').remove();
    showtable(studentId, yearsValue, saValue)
}

function showtable(studentId, yearsValues, saValues) {
    $.ajax({
        url: '/QMyScore',
        type: 'POST',
        data: {
            studentId: studentId,
            yearsValue: yearsValues,
            saValue: saValues
        },
        dataType: 'json',
        success: function (data) {

            for (var i in data) {
                let Tid = data[i][0];
                let Cname = data[i][1];
                let credit = data[i][2];
                let Tname = data[i][3];
                if(Tname == '1'){
                    Tname = '正常考试'
                }else if(Tname == '2'){
                    Tname = '补考'
                }else if(Tname == '3'){
                    Tname = '缓考'
                }
                Cname = JSON.parse(Cname)
                if (Cname < 60) {
                    TS += TableString.replace('{%Tid%}', Tid)
                    .replace('{%Cname%}', Cname)
                    .replace('{%credit%}', credit)
                    .replace('{%Tname%}', Tname)
                    .replace('pass','fail');
                } else {
                    TS += TableString.replace('{%Tid%}', Tid)
                    .replace('{%Cname%}', Cname)
                    .replace('{%credit%}', credit)
                    .replace('{%Tname%}', Tname);
                }
            }
            $('.card-block table').append(TS);
            TS = '';
        },
        error: function (err) {
            console.log(err)
        }
    })
}