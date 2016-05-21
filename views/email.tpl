% rebase('base.tpl', title='CWD Email List', refreshinterval=0, scripturl='')
<div class="container">
    <h5 class="center-align">Emails</h5>
    <table class="responsive-table highlight bordered">
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Jobname Match</th>
            <th>Active</th>
            <th>Edit/Add</th>
        </tr>
% for email in emaillist:
        <tr>
            <td>{{ email.name }}</a></td>
            <td>{{ email.emailaddress }}</td>
            <td>{{ email.namematch }}</td>
            <td>{{ email.active }}</td>
            <td><a class="btn-floating waves-effect waves-light red" href="{{get_url("/emaildelete/<id>", id=email.id)}}"><i class="material-icons">delete</i></a>
            <a class="btn-floating waves-effect waves-light blue" href="{{get_url("/emailform/<id>", id=email.id) }}"><i class="material-icons">mode_edit</i></a>
            </td>
        </tr>
% end
    </table>
    <div class="fixed-action-btn" style="bottom: 45px; right: 24px;">
        <a class="btn-floating btn-large waves-effect waves-light red" href="{{get_url("/emailform")}}">
            <i class="large material-icons">mode_edit</i>
        </a>
    </div>
</div>