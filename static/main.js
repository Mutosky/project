function lineChart(){
    new Vue({
        el: '#app',
        data: function () {
            return {
                chartData: {
                    columns: ['date', 'sales'],
                    rows: [
                        { 'date': '1月1日', 'sales': 123 },
                        { 'date': '1月2日', 'sales': 1223 },
                        { 'date': '1月3日', 'sales': 2123 },
                        { 'date': '1月4日', 'sales': 4123 },
                        { 'date': '1月5日', 'sales': 3123 },
                        { 'date': '1月6日', 'sales': 7123 }
                    ]
                }
            }
        },
        components: { VeLine }
    })
}




function pieChart(label1, label2, label3, data1, data2, data3, elementid) {
    const ctx = document.getElementById(elementid).getContext('2d');
    const data = {
        labels: [label1, label2, label3],
        datasets: [{
            data: [data1, data2, data3],
            backgroundColor: ['blue', 'orange', 'red']
        }]
    };

    const myChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        option: {
            //optional
        }
    });
    return {
        myChart
    }
}





function signIn(){
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if(username && password){
        fetch('/login', {
            method: 'POST',
            body: JSON.stringify({name: username, pass: password}),
            headers: {'content-Type': 'application/json'}
        });
    }

}






function signUp(){
    const username = document.getElementById('username-signup').value;
    const password = document.getElementById('password-signup').value;
    const conPassword = document.getElementById('conpassword-signup').value;

    if (username && password && conPassword){
        if(password === conPassword){
            fetch('/signup', {
                method: 'POST',
                body: JSON.stringify({name: username, pass: password}),
                headers: {'content-type': 'application/json'}
            });
        }
    }
}





async function getSelectedTeams(){
    const selectedTeam1 = document.getElementById('Team1');
    const selectedTeam2 = document.getElementById('Team2');
    const team1Selected = selectedTeam1.value;
    const team2Selected = selectedTeam2.value;

    if(team1Selected && team2Selected){
        const response = await fetch('/home', {
            method: 'POST',
            body: JSON.stringify({team1: team1Selected, team2: team2Selected}),
            headers: {'Content-Type': 'application/json'}
        });
        if(!response.ok){
            throw new Error(`Error: ${response.status}`);
        }

        const jsonData = await response.json();
        const h2hData = jsonData['H2H_data']['last_match_probability'];
        const homeTeam = h2hData[1] * 100
        const awayTeam = h2hData[0] * 100
        const draw = h2hData[2] * 100

        let label1 = 'draw';
        let label2 = 'Home';
        let label3 = 'Away';
        let data1 = draw;
        let data2 = homeTeam;
        let data3 = awayTeam;
        let elementid = 'chart-container';

        pieChart(label1, label2, label3, data1, data2, data3, elementid)

    }
}