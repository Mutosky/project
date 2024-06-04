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
    const SMopponentN = document.getElementById('team1opponent');
    const SMopponentN2 = document.getElementById('team2opponent');

    text.innerHTML = `${teamHome} last match`;
    text1.innerHTML = `${teamAway} last match`;
    text2.innerHTML = `${teamHome} last five match`;
    text3.innerHTML = `${teamAway} last five match`;
    text4.innerHTML = `${teamHome} home advantage`;
    SMopponentN.innerHTML = teamHome;
    SMopponentN2.innerHTML = teamAway;

}




async function similarOppponet(team1Name, team2Name){
    const respond = await fetch('/similaropponent', {
        method: 'POST',
        body: JSON.stringify({team1: team1Name, team2: team2Name}),
        headers: {'Content-Type': 'application/json'}
    });
    const datas = await respond.json();
    const opponentNameL = document.getElementById('oppoName');

    let OD  = datas['opponent']['data']; 

    opponentNameL.innerHTML = '';
    OD.forEach(data => {
        const button = document.createElement('button');
        const list = document.createElement('li')
        const h11 = document.createElement('h2');
        const h12 = document.createElement('h2');
        const h13 = document.createElement('h2');
        const h14 = document.createElement('h2');

        button.textContent = data.name;
        button.addEventListener('click', () => piedatachange(OD, datas, data.name));
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
    pieChart('win', 'loss', 'draw', datas['team1']['win'][0] * 100, datas['team1']['loss'][0] * 100, datas['team1']['draw'][0] * 100, 'homeTeamSO');
    pieChart('win', 'loss', 'draw', datas['team2']['win'][0] * 100, datas['team2']['loss'][0] * 100, datas['team2']['draw'][0] * 100, 'awayTeamSO');
}
function piedatachange(OD, datas, name){
    console.log(OD.name);
    if (name === OD[0].name){
        pieChart('win', 'loss', 'draw', datas['team1']['win'][0] * 100, datas['team1']['loss'][0] * 100, datas['team1']['draw'][0] * 100, 'homeTeamSO');
        pieChart('win', 'loss', 'draw', datas['team2']['win'][0] * 100, datas['team2']['loss'][0] * 100, datas['team2']['draw'][0] * 100, 'awayTeamSO');
    } else if (name === OD[1].name) {
        pieChart('win', 'loss', 'draw', datas['team1']['win'][1] * 100, datas['team1']['loss'][1] * 100, datas['team1']['draw'][1] * 100, 'homeTeamSO');
        pieChart('win', 'loss', 'draw', datas['team2']['win'][1] * 100, datas['team2']['loss'][1] * 100, datas['team2']['draw'][1] * 100, 'awayTeamSO');
    } else if (name === OD[2].name) {
        pieChart('win', 'loss', 'draw', datas['team1']['win'][2] * 100, datas['team1']['loss'][2] * 100, datas['team1']['draw'][2] * 100, 'homeTeamSO');
        pieChart('win', 'loss', 'draw', datas['team2']['win'][2] * 100, datas['team2']['loss'][2] * 100, datas['team2']['draw'][2] * 100, 'awayTeamSO');
    } else if (name === OD[3].name) {
        pieChart('win', 'loss', 'draw', datas['team1']['win'][3] * 100, datas['team1']['loss'][0] * 100, datas['team1']['draw'][3] * 100, 'homeTeamSO');
        pieChart('win', 'loss', 'draw', datas['team2']['win'][3] * 100, datas['team2']['loss'][0] * 100, datas['team2']['draw'][3] * 100, 'awayTeamSO');
    } else if (name === OD[4].name) {
        pieChart('win', 'loss', 'draw', datas['team1']['win'][4] * 100, datas['team1']['loss'][0] * 100, datas['team1']['draw'][4] * 100, 'homeTeamSO');
        pieChart('win', 'loss', 'draw', datas['team2']['win'][4] * 100, datas['team2']['loss'][0] * 100, datas['team2']['draw'][4] * 100, 'awayTeamSO');
    } 

}



async function displayH2H(team1Name, team2Name){
    const respond = await fetch('/head2head', {
        method: 'POST',
        body: JSON.stringify({ team1: team1Name, team2: team2Name }),
        headers: { 'Content-Type': 'application/json' }
    });
    const datas = await respond.json();
    if (datas['status'] === 500){
        let displayid1 = 'date-list';
        let displayid2 = 'outcome-list';
        listDisplay(displayid1, ['no', 'data', 'found']);
        listDisplay(displayid2, ['having', 'problem', 'getting', 'H2H data']);
    } else{
        const outcome = datas['match_outcome'];
        const h2hData = datas['datalist'];
        const date = datas['event_date'];
        pieChart('draw', 'Home', 'Away', h2hData[2] * 100, h2hData[1] * 100, h2hData[0] * 100, 'chart-container');
        let displayid1 = 'date-list';
        let displayid2 = 'outcome-list';
        listDisplay(displayid1, date);
        listDisplay(displayid2, outcome);
    }
}



async function displayPFM(team1Name){
    const respond = await fetch('/pastFiveMatch', {
        method: 'POST',
        body: JSON.stringify({ team1: team1Name }),
        headers: { 'Content-Type': 'application/json' }
    });
    const datas = await respond.json();


    pieChart('win', 'loss', 'draw', datas['win'][0] * 100, datas['loss'][0] * 100, datas['draw'][0] * 100, 'bar-container');
    lineChart(datas['date'][0], datas['date'][1], datas['date'][2], datas['date'][3], datas['date'][4], datas['win'], datas['loss'], datas['draw'], 'home-myChart');

    listDisplay('homeLFList1', datas['opponent']);
    listDisplay('homeLFList2', datas['outcome']);
    listDisplay('homeLFList3', datas['date']);

}



async function displayHAT(team1Name){
    const respond = await fetch('/homeAdvantages', {
        method: 'POST',
        body: JSON.stringify({ team1: team1Name }),
        headers: { 'Content-Type': 'application/json' }
    });
    const datas = await respond.json();

    lineChart(datas['date'][0], datas['date'][1], datas['date'][2], datas['date'][3], datas['date'][4], datas['win'], datas['loss'], datas['draw'], 'homeAdata');
    let displayid3 = 'homeAList';
    let displayid4 = 'homeAListB';
    let displayid5 = 'homeAListC';

    listDisplay(displayid3, datas['date']);
    listDisplay(displayid4, datas['outcome']);
    listDisplay(displayid5, datas['opponent']);

}



async function displayPFM2(team2Name) {
    const respond = await fetch('/pastFiveMatch', {
        method: 'POST',
        body: JSON.stringify({ team1: team2Name }),
        headers: { 'Content-Type': 'application/json' }
    });
    const datas = await respond.json()


    pieChart('win', 'loss', 'draw', datas['win'][0] * 100, datas['loss'][0] * 100, datas['draw'][0] * 100, 'bar-containers');
    lineChart(datas['date'][0], datas['date'][1], datas['date'][2], datas['date'][3], datas['date'][4], datas['win'], datas['loss'], datas['draw'], 'away-myChart');

    listDisplay('awayLFList1', datas['opponent']);
    listDisplay('awayLFList2', datas['outcome']);
    listDisplay('awayLFList3', datas['date']);


}



function loadings(load=true){
    const loading = document.getElementById('loadingState');
    if(load){
        loading.style.display = 'block';
        loading.innerHTML = 'loading....';
        loading.innerHTML = 'loading.....';
        loading.innerHTML = 'loading......';
        loading.innerHTML = 'loading.......';
    } else {
        loading.style.display = 'none';
    }

}



async function getSelectedTeams(){
    const throbber = document.getElementById('throbber-overlay');

    const selectedTeam1 = document.getElementById('Team1');
    const selectedTeam2 = document.getElementById('Team2');

    const team1Selected = selectedTeam1.value;
    const team2Selected = selectedTeam2.value;
    if (team1Selected === team2Selected){
        alert('select two different teams');
    } else {
        if (team1Selected && team2Selected) {
            throbber.style.display = 'block';
            loadings(true);
            textDisplay(team1Selected, team2Selected);
            await displayHAT(team1Selected);
            await displayH2H(team1Selected, team2Selected);
            await displayPFM(team1Selected);
            await similarOppponet(team1Selected, team2Selected);
            await displayPFM2(team2Selected);
            loadings(false);
            throbber.style.display = 'none';
            alert('data received successfully');
        }
    }
}