% rebase('base.tpl', title='CWD Job Summary', refreshinterval=120, scripturl='')
<div class="container">
    <h5 class="center-align">Jobs</h5>
    <table class="responsive-table highlight bordered">
        <tr>
            <th>Job</th>
            <th>Last Event Time</th>
            <th>Last Run Time (s)</th>
            <th>Last Status</th>
            <th>Max Runtime (s)</th>
            <th>Min Runtime (s)</th>
            <th>SLA (min)</th>
            <th>Period (min)</th>
            <th>Active</th>
            <th>Edit</th>
        </tr>
        % for job in joblist:
        <tr>
            <td><a href="{{ get_url('/jobs/<name>', name=job.name) }}">{{ job.name }}</a></td>
            <td>{{ str(job.eventtime)[0:19] }}</td>
            <td>{{ job.runtime }}</td>
            <td><div class="chip {{!"green" if job.status == 'end' else "red"}}">{{ statuslookup[job.status] }}</div></td>
            <td>{{ job.maxruntime }}</td>
            <td>{{ job.minruntime }}</td>
            <td>{{ job.sla }}</td>
            <td>{{ job.period }}</td>
            <td>{{ job.active }}</td>
            <td><a class="btn-floating waves-effect waves-light blue" href="{{ get_url('/jobform/<name>', name=job.name) }}"><i class="material-icons">mode_edit</i></a>
            </td>
        </tr>
        % end
    </table>
    <div>Jobs will be added automatically from client side updates. Period and SLA can be edited here.</div>

</div>