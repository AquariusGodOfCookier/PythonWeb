var TableString = `
<tr>
<td>{%subjectName%}</td>
<td>{%StudentId%}</td>
<td>{%StudentName%}</td>
<td><input type="text" {%readonly%} value="{%grade%}" style="width:80px;padding-left:10px;"></td>
<td><button onclick="xiugai('{%cid%}','{%sid%}')">修改成绩</button></td>
</tr>
`;
$(function () {
    try {
        cookieContent = get_cookie('WTF');
        if (cookieContent == undefined) {
            alert('请先去登录')
            window.location.href = '/'
        }
        cookieContent = cookieContent.replace('[', '').replace(']', '').replace(/"/g, '').split(',');
        teachername = $.trim(cookieContent[1]);
        teacherid = $.trim(cookieContent[0])
        document.getElementsByClassName('WelCome')[0].innerHTML = '欢迎' + teachername + '老师登录';
        $.ajax({
            url: '/Qteacher',
            type: 'POST',
            data: {
                teacherid: teacherid,
            },
            dataType: 'json',
            success: function (data) {
                let cc = 0;
                let ccc = [];
                window.aaa = [];
                aaa[0] = 'null'
                for (let i in data) {
                    let subjects = i;
                    let students = data[i][0];
                    ccc.push(i)
                    for (let index in students) {
                        let StudentId = students[index][0]
                        let Studentname = students[index][1]
                        let StudnetGrade = students[index][2]
                        if (StudnetGrade == 'none') {
                            StudnetGrade = '暂无成绩'
                        }
                        aaa.push({
                            i,
                            StudentId,
                            Studentname,
                            StudnetGrade
                        })
                    }
                }
                //写分页 
                var PageLinkNum = Math.ceil(aaa.length / 3);
                var PageStr = '';
                var str = ''
                var astr = ''
                for (var Pageindex = 1; Pageindex <= PageLinkNum; Pageindex++) {
                    PageStr += '<li class="page-item"><a class="page-link" data-page="' + Pageindex + '" href="#">' + Pageindex + '</a></li>'
                }
                for (var i = 0; i < ccc.length; i++) {
                    str += '<option value="' + i + '">' + ccc[i] + '</option>'
                }
                for (var i = 1; i <= 3; i++) {
                    let asd = Number(aaa[i]['Studentname'])
                    if(isNaN(asd)){
                        console.log(asd)
                    }else{
                        console.log('dd')
                    }
                    astr += TableString.replace('{%subjectName%}', aaa[i]['i'])
                        .replace('{%StudentId%}', aaa[i]['StudentId'])
                        .replace('{%StudentName%}', aaa[i]['Studentname'])
                        .replace('{%grade%}', aaa[i]['StudnetGrade'])
                        .replace('{%cid%}',aaa[i]['i'])
                        .replace('{%sid%}',aaa[i]['StudentId'])
                }
                console.log(aaa)
                $('.pagination-sm').append(PageStr)
                $('#WhatSub').append(str)
                $('.col-12 table').append(astr)
            },
            error: function (err) {
                console.log(err)
            }
        })
    } catch {
        window.location.href = '/';
    }
})
// 123 1
// 456 2
// 789 3
// 10  4

var pageItem = document.getElementsByClassName('pagination-sm')[0];
pageItem.addEventListener('click', function (ev) {
    var ev = ev || window.event;
    var target = ev.target || ev.srcElement;
    var astr = '';
    $('.col-12 table td').remove();
    if (target.nodeName.toLowerCase() == 'a') {
        let APageIndex = Number(target.getAttribute('data-page'));
        let BPageIndex = 1 + 3 * (APageIndex - 1)
        for (var i = BPageIndex; i < Number(BPageIndex) + 3; i++) {
            if (aaa[i] == undefined) {
                return
            } else {
                astr += TableString.replace('{%subjectName%}', aaa[i]['i'])
                    .replace('{%StudentId%}', aaa[i]['StudentId'])
                    .replace('{%StudentName%}', aaa[i]['Studentname'])
                    .replace('{%grade%}', aaa[i]['StudnetGrade'])
                    .replace('{%cid%}',aaa[i]['i'])
                    .replace('{%sid%}',aaa[i]['StudentId'])
            }
            $('.col-12 table').append(astr)
            astr = ''
        }
    } else {
        alert('我也不知道怎么禁止点击ul，很烦,所以我就让他跳到第一页了，嗯，就这样,希望我能想到好的方法')
        for (var i = 1; i < 4; i++) {
            if (aaa[i] == undefined) {
                return
            } else {
                astr += TableString.replace('{%subjectName%}', aaa[i]['i'])
                    .replace('{%StudentId%}', aaa[i]['StudentId'])
                    .replace('{%StudentName%}', aaa[i]['Studentname'])
                    .replace('{%grade%}', aaa[i]['StudnetGrade'])
            }
            $('.col-12 table').append(astr)
            astr = ''
        }
    }
})

function chaxun() {
    // $('.col-12 table').append('');
    $('.col-12 table td').remove();
    var WhatSub = document.getElementById('WhatSub');
    var index = WhatSub.selectedIndex;
    var WhatSubValue = WhatSub.options[index].innerHTML;
    var strs = ''
    for (var i in aaa) {
        if (aaa[i]['i'] == WhatSubValue) {
            strs += TableString.replace('{%subjectName%}', aaa[i]['i'])
                .replace('{%StudentId%}', aaa[i]['StudentId'])
                .replace('{%StudentName%}', aaa[i]['Studentname'])
                .replace('{%grade%}', aaa[i]['StudnetGrade'])
        }
    }
    $('.col-12 table').append(strs)
    strs = ''
}

function xiugai(cname,sid){
    let inputs = $(event.currentTarget).parent().parent().find('input').val();
    let numinputs = Number(inputs)
    if(isNaN(numinputs) || numinputs<0||numinputs>100){
        alert('你输入的得分情况错误，请检查后输入修改')
    }else{
        $.ajax({
            url: '/Cgrade',
            type: 'POST',
            data: {
               cname :cname,
               sid:sid,
               numinputs:numinputs
            },
            dataType: 'text',
            success:function(data){
                if(data=='ok'||data=='AlertGradeSuccess'){
                    alert('修改成功,刷新后生效，也可以不刷新，一起修改之后刷新')
                }else{
                    alert('修改失败')
                }
                console.log(data)
            },
            error:function(err){
                console.log(err)
            }
        })
    }
}