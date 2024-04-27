function lineChart(match1, match2, match3, match4, match5, winData, lossData, drawData, elementId) {
    const ctx = document.getElementById(elementId).getContext('2d');
    ctx.innerHTML = '';

    // Sample data for wins, losses, and draws (replace with your actual data)

    const labels = [match1, match2, match3, match4, match5];

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Wins',
                data: winData,
                borderColor: 'green',
                backgroundColor: 'rgba(0, 255, 0, 0.2)', // Transparent green fill
                fill: false, // Fill the area under the line
            },
            {
                label: 'Losses',
                data: lossData,
                borderColor: 'red',
                backgroundColor: 'rgba(255, 0, 0, 0.2)', // Transparent red fill
                fill: false, // Fill the area under the line
            },
            {
                label: 'Draws',
                data: drawData,
                borderColor: 'grey',
                backgroundColor: 'rgba(128, 128, 128, 0.2)', // Transparent grey fill
                fill: false, // Fill the area under the line
            },
        ],
    };

    const myChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
        },
    });
    return {
        myChart
    }
}






function pieChart(label1, label2, label3, data1, data2, data3, elementid) {
    const ctx = document.getElementById(elementid).getContext('2d');
    ctx.innerHTML = '';
    const data = {
        labels: [label1, label2, label3],
        datasets: [{
            data: [data1, data2, data3],
            backgroundColor: ['green', 'red', 'brown']
        }]
    };

    const myChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        option: {
            maintainAspectRatio: false,
            width: 400,
            height: 400
        },
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
        const last5MatchAway = jsonData['Lastfivematchdata']['AwayTeam'];
        const last5MatchHome = jsonData['Lastfivematchdata']['HomeTeam'];
        const dates = last5MatchHome['date'];
        const dates2 = last5MatchAway['date'];


        const homeTeamData={
            'win': last5MatchHome['win'],
            'loss': last5MatchHome['loss'],
            'draw': last5MatchHome['draw'],
            'Id': 'home-myChart'

        }

        const awayTeamData ={
            'win': last5MatchAway['win'],
            'loss': last5MatchAway['loss'],
            'draw': last5MatchAway['draw'],
            'Id': 'away-myChart'
        }

        const homeTeam = h2hData[1] * 100;
        const awayTeam = h2hData[0] * 100;
        const draw = h2hData[2] * 100;

        const teamHome = jsonData['H2H_data']['team1'][0];
        const teamAway = jsonData['H2H_data']['team2'][0];

        const text = document.getElementById('home-label');
        const text1 = document.getElementById('away-label');
        const text2 = document.getElementById('home-lastfive');
        const text3 = document.getElementById('away-lastfive');

        text.innerHTML = '';
        text1.innerHTML = '';
        text2.innerHTML = '';
        text3.innerHTML = '';


        let label1 = 'draw';
        let label2 = 'Home';
        let label3 = 'Away';
        let data1 = draw;
        let data2 = homeTeam;
        let data3 = awayTeam;
        let elementid = 'chart-container';

        pieChart(label1, label2, label3, data1, data2, data3, elementid);
        lineChart(dates[0], dates[1], dates[2], dates[3], dates[4], homeTeamData['win'], homeTeamData['loss'], homeTeamData['draw'], homeTeamData['Id']);
        lineChart(dates2[0], dates2[1], dates2[2], dates2[3], dates2[4], awayTeamData['win'], awayTeamData['loss'], awayTeamData['draw'], awayTeamData['Id']);

        pieChart('win', 'loss', 'draw', homeTeamData['win'][0]*100, homeTeamData['loss'][0]*100, homeTeamData['draw'][0]*100, 'bar-container');
        pieChart('win', 'loss', 'draw', awayTeamData['win'][0]*100, awayTeamData['loss'][0]*100, awayTeamData['draw'][0]*100, 'bar-containers');
        
        text.innerHTML = `${teamHome} last match`;
        text1.innerHTML = `${teamAway} last match`;
        text2.innerHTML = `${teamHome} last five match`;
        text3.innerHTML = `${teamAway} last five match`;


        const matchList = document.getElementById('');
        matchList.innerHTML = '';





    }
}