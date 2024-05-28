function lineChart(match1, match2, match3, match4, match5, winData, lossData, drawData, elementId) {
    const ctx = document.getElementById(elementId).getContext('2d');
    const existingChart = Chart.getChart(ctx);


    const labels = [match1, match2, match3, match4, match5];

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Wins',
                data: winData,
                borderColor: 'green',
                backgroundColor: 'rgba(0, 255, 0, 0.2)',
                fill: false,
            },
            {
                label: 'Losses',
                data: lossData,
                borderColor: 'red',
                backgroundColor: 'rgba(255, 0, 0, 0.2)', 
                fill: false, 
            },
            {
                label: 'Draws',
                data: drawData,
                borderColor: 'grey',
                backgroundColor: 'rgba(128, 128, 128, 0.2)', // Transparent grey fill
                fill: false, 
            },
        ],
    };

    if(existingChart){
        existingChart.data = data;
        existingChart.update();
    } else{
        new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
            },
        });
    }

}






function pieChart(label1, label2, label3, data1, data2, data3, elementid) {
    const ctx = document.getElementById(elementid).getContext('2d');
    const existingChart = Chart.getChart(ctx);

    const data = {
        labels: [label1, label2, label3],
        datasets: [{
            data: [data1, data2, data3],
            backgroundColor: ['green', 'red', 'brown']
        }]
    };

    if(existingChart){
        existingChart.data = data;
        existingChart.update();
    } else {
        new Chart(ctx, {
            type: 'pie',
            data: data,
            option: {
                maintainAspectRatio: false,
                width: 400,
                height: 400
            },
        });
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
        })
        .then(respond => respond.json())
        .then(data => {
            if(data.redirect){
                window.location.href = data.redirect;
            } else if(data.error){
                alert(data.error);
            }
        })
    } else {
        alert('please input your username and password')
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
            })
            .then(respond => respond.json())
            .then(data => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else if (data.error) {
                    alert(data.error);
                }
            })

        } else {
            alert('password does not match')
        }
    } else {
        alert('please input all information asked')
    }
}



function toggleMenu() {
    var menu = document.querySelector('.menu');
    menu.classList.toggle('show');
}


function listDisplay(elementId, datas){
    const typeList = document.getElementById(elementId);
    typeList.innerHTML = '';
    datas.forEach(data => {
        list = document.createElement('li');
        list.textContent = data;
        typeList.appendChild(list);
    })
}


function textDisplay(teamHome, teamAway){
    const text = document.getElementById('home-label');
    const text1 = document.getElementById('away-label');
    const text2 = document.getElementById('home-lastfive');
    const text3 = document.getElementById('away-lastfive');
    const text4 = document.getElementById('dataLabel');

    text.innerHTML = `${teamHome} last match`;
    text1.innerHTML = `${teamAway} last match`;
    text2.innerHTML = `${teamHome} last five match`;
    text3.innerHTML = `${teamAway} last five match`;
    text4.innerHTML = `${teamHome} home advantage`;

}

function similarOppponet(datas){
    const opponentNameL = document.getElementById('oppoName');
    let OD  = datas['opponents']['data']; 

    opponentNameL.innerHTML = '';
    OD.forEach(data => {
        const button = document.createElement('button');
        const list = document.createElement('li')
        const h11 = document.createElement('h2');
        const h12 = document.createElement('h2');
        const h13 = document.createElement('h2');
        const h14 = document.createElement('h2');

        button.textContent = data.name;
        button.addEventListener('click', () => piedatachange(OD, datas, data.name))
        h11.textContent = data.team1Date;
        h12.textContent = data.team1Outcome;
        h13.textContent = data.team2Date;
        h14.textContent = data.team2Outcome;

        list.appendChild(button);
        list.appendChild(h11);
        list.appendChild(h12);
        list.appendChild(h13);
        list.appendChild(h14);
        opponentNameL.appendChild(list)


    })

    pieChart('win', 'loss', 'draw', datas['teamOne']['win'][0] * 100, datas['teamOne']['loss'][0] * 100, datas['teamOne']['draw'][0] * 100, 'homeTeamSO');
    pieChart('win', 'loss', 'draw', datas['teamTwo']['win'][0] * 100, datas['teamTwo']['loss'][0] * 100, datas['teamTwo']['draw'][0] * 100, 'awayTeamSO');
}

function piedatachange(OD, datas, name){
    console.log(OD.name);
    if (name === OD[0].name){
        pieChart('win', 'loss', 'draw', datas['teamOne']['win'][0] * 100, datas['teamOne']['loss'][0] * 100, datas['teamOne']['draw'][0] * 100, 'homeTeamSO');
        pieChart('win', 'loss', 'draw', datas['teamTwo']['win'][0] * 100, datas['teamTwo']['loss'][0] * 100, datas['teamTwo']['draw'][0] * 100, 'awayTeamSO');
    } else if (name === OD[1].name) {
        pieChart('win', 'loss', 'draw', datas['teamOne']['win'][1] * 100, datas['teamOne']['loss'][1] * 100, datas['teamOne']['draw'][1] * 100, 'homeTeamSO');
        pieChart('win', 'loss', 'draw', datas['teamTwo']['win'][1] * 100, datas['teamTwo']['loss'][1] * 100, datas['teamTwo']['draw'][1] * 100, 'awayTeamSO');
    } else if (name === OD[2].name) {
        pieChart('win', 'loss', 'draw', datas['teamOne']['win'][2] * 100, datas['teamOne']['loss'][2] * 100, datas['teamOne']['draw'][2] * 100, 'homeTeamSO');
        pieChart('win', 'loss', 'draw', datas['teamTwo']['win'][2] * 100, datas['teamTwo']['loss'][2] * 100, datas['teamTwo']['draw'][2] * 100, 'awayTeamSO');
    } else if (name === OD[3].name) {
        pieChart('win', 'loss', 'draw', datas['teamOne']['win'][3] * 100, datas['teamOne']['loss'][0] * 100, datas['teamOne']['draw'][3] * 100, 'homeTeamSO');
        pieChart('win', 'loss', 'draw', datas['teamTwo']['win'][3] * 100, datas['teamTwo']['loss'][0] * 100, datas['teamTwo']['draw'][3] * 100, 'awayTeamSO');
    } else if (name === OD[4].name) {
        pieChart('win', 'loss', 'draw', datas['teamOne']['win'][4] * 100, datas['teamOne']['loss'][0] * 100, datas['teamOne']['draw'][4] * 100, 'homeTeamSO');
        pieChart('win', 'loss', 'draw', datas['teamTwo']['win'][4] * 100, datas['teamTwo']['loss'][0] * 100, datas['teamTwo']['draw'][4] * 100, 'awayTeamSO');
    } 

}


async function getSelectedTeams(){
    const throbber = document.getElementById('throbber-overlay');

    const selectedTeam1 = document.getElementById('Team1');
    const selectedTeam2 = document.getElementById('Team2');

    const loading = document.getElementById('loadingState');
    
    const team1Selected = selectedTeam1.value;
    const team2Selected = selectedTeam2.value;
    loading.innerHTML = 'loadin..';
    if (team1Selected === team2Selected){
        alert('select two different teams');
    } else {
        loading.innerHTML = 'loading...';
        if (team1Selected && team2Selected) {
            throbber.style.display = 'block';
            try {
                const response = await fetch('/footballanalysis', {
                    method: 'POST',
                    body: JSON.stringify({ team1: team1Selected, team2: team2Selected }),
                    headers: { 'Content-Type': 'application/json' }
                });
                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }
                
                loading.innerHTML='collecting data....';
                const jsonData = await response.json();
                const h2hData = jsonData['H2H_data']['last_match_probability'];
                const outcome = jsonData['H2H_data']['outcome'];
                const date = jsonData['H2H_data']['date'];
                const last5MatchAway = jsonData['Lastfivematchdata']['AwayTeam'];
                const last5MatchHome = jsonData['Lastfivematchdata']['HomeTeam'];
                const homeData = jsonData['homeAdvange']
                const datesadvan = homeData['date']
                const outcomeadvan = homeData['match_outcome']
                const opponentL = homeData['opponent']
                const homeDates = homeData['date']
                const dates = last5MatchHome['date'];
                const dates2 = last5MatchAway['date'];
                const similarOD = jsonData['similarOpponent'];


                loading.innerHTML='processing data.....';
                const homeTeamData = {
                    'win': last5MatchHome['win'],
                    'loss': last5MatchHome['loss'],
                    'draw': last5MatchHome['draw'],
                    'Id': 'home-myChart'

                }

                const awayTeamData = {
                    'win': last5MatchAway['win'],
                    'loss': last5MatchAway['loss'],
                    'draw': last5MatchAway['draw'],
                    'Id': 'away-myChart'
                }

                const homeAdvantage = {
                    'win': homeData['win'],
                    'loss': homeData['loss'],
                    'draw': homeData['draw'],
                    'Id': 'homeAdata'
                }


                loading.innerHTML='displaying data';
                pieChart('draw', 'Home', 'Away', h2hData[2] * 100, h2hData[1] * 100, h2hData[0] * 100, 'chart-container');
                lineChart(dates[0], dates[1], dates[2], dates[3], dates[4], homeTeamData['win'], homeTeamData['loss'], homeTeamData['draw'], homeTeamData['Id']);
                lineChart(dates2[0], dates2[1], dates2[2], dates2[3], dates2[4], awayTeamData['win'], awayTeamData['loss'], awayTeamData['draw'], awayTeamData['Id']);
                lineChart(homeDates[0], homeDates[1], homeDates[2], homeDates[3], homeDates[4], homeAdvantage['win'], homeAdvantage['loss'], homeAdvantage['draw'], homeAdvantage['Id']);

                pieChart('win', 'loss', 'draw', homeTeamData['win'][0] * 100, homeTeamData['loss'][0] * 100, homeTeamData['draw'][0] * 100, 'bar-container');
                pieChart('win', 'loss', 'draw', awayTeamData['win'][0] * 100, awayTeamData['loss'][0] * 100, awayTeamData['draw'][0] * 100, 'bar-containers');

                textDisplay(jsonData['H2H_data']['team1'][0], jsonData['H2H_data']['team2'][0]);


                let displayid1 = 'date-list';
                let displayid2 = 'outcome-list';
                let displayid3 = 'homeAList';
                let displayid4 = 'homeAListB';
                let displayid5 = 'homeAListC';

                listDisplay(displayid1, date);
                listDisplay(displayid2, outcome);
                listDisplay(displayid3, datesadvan);
                listDisplay(displayid4, outcomeadvan);
                listDisplay(displayid5, opponentL);



                listDisplay('homeLFList1', last5MatchHome['opponent']);
                listDisplay('homeLFList2', last5MatchHome['Outcome']);
                listDisplay('homeLFList3', dates);
                listDisplay('awayLFList1', last5MatchAway['opponent']);
                listDisplay('awayLFList2', last5MatchAway['Outcome']);
                listDisplay('awayLFList3', dates2);

                similarOppponet(similarOD);

                loading.innerHTML='completed!';

            } finally {
                throbber.style.display = 'none';
            }
        }
    }
}