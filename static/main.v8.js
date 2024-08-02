function chart(winP, lossP, drawP){
    const progressContainer = document.createElement('div');
    progressContainer.className = 'progress-container';

    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';

    const winLabel = document.createElement('div');
    winLabel.textContent = `win ${winP*100}%` ;
    winLabel.className = 'label';

    const lossLabel = document.createElement('div');
    lossLabel.textContent = `loss ${lossP*100}%`;
    lossLabel.className = 'label';

    const drawLabel = document.createElement('div');
    drawLabel.textContent = `draw ${drawP*100}%`;
    drawLabel.className = 'label';
    
    const winPro = document.createElement('div');
    winPro.className = 'progress win';
    winPro.style.width = `${winP*100}%`;

    const drawPro = document.createElement('div');
    drawPro.className = 'progress draw';
    drawPro.style.width = `${drawP*100}%`;

    const lossPro = document.createElement('div');
    lossPro.className = 'progress loss';
    lossPro.style.width =`${lossP*100}%`;
    
    progressBar.appendChild(winPro);
    progressBar.appendChild(drawPro);
    progressBar.appendChild(lossPro);
    progressContainer.appendChild(winLabel);
    progressContainer.appendChild(drawLabel);
    progressContainer.appendChild(lossLabel);
    progressContainer.appendChild(progressBar);

    return progressContainer;

}

function toggleMenu() {
    var menu = document.querySelector('.menu');
    menu.classList.toggle('show');
}






async function similarOppponet(team1Name, team2Name){
    const divID = document.getElementById('SMOdata');
    
    const respond = await fetch('/similaropponent', {
        method: 'POST',
        body: JSON.stringify({team1: team1Name, team2: team2Name}),
        headers: {'Content-Type': 'application/json'}
    });

    const datas = await respond.json();
    if ('team1' in datas){
        const maxLength = Math.min(datas.team1.win.length, datas.team2.win.length, datas.team1.loss.length, datas.team2.loss.length);
        const dataList = datas['opponent']['data'];
        for(let i=0; i<maxLength; i++){
            const container = document.createElement('div');
            container.className = 'SMOcontain';

            const team1TextDiv = document.createElement('div');
            team1TextDiv.className = 'textDiv';
            const team1Outcome = document.createElement('h1');
            team1Outcome.textContent = `outcome: ${dataList[i].team1Outcome}`;
            const team1Date = document.createElement('h1');
            team1Date.textContent = `date: ${dataList[i].team1Date}`;
            team1TextDiv.appendChild(team1Outcome);
            team1TextDiv.appendChild(team1Date);

            const team2TextDiv = document.createElement('div');
            team2TextDiv.className = 'textDiv';
            const team2Outcome = document.createElement('h1');
            team2Outcome.textContent = `outcome: ${dataList[i].team2Outcome}`;
            const team2Date = document.createElement('h1');
            team2Date.textContent = `date: ${dataList[i].team2Date}`;
            team2TextDiv.appendChild(team2Outcome);
            team2TextDiv.appendChild(team2Date);

            const team1Names = document.createElement('h1');
            team1Names.className = 'teamName';
            team1Names.textContent = team1Name;

            const team2Names = document.createElement('h1');
            team2Names.className = 'teamName';
            team2Names.textContent = team2Name;

            const opponentName = document.createElement('h1');
            opponentName.className = 'opponentname';
            opponentName.textContent = dataList[i].name;

            const team1ProgressContainer = chart(datas.team1.win[i], datas.team1.loss[i], datas.team1.draw[i]);
            const team2ProgressContainer = chart(datas.team2.win[i], datas.team2.loss[i], datas.team2.draw[i]);

            container.appendChild(opponentName);
            container.appendChild(team1Names);
            container.appendChild(team1ProgressContainer);
            container.appendChild(team1TextDiv);
            container.appendChild(team2Names);
            container.appendChild(team2ProgressContainer);
            container.appendChild(team2TextDiv);

            divID.appendChild(container);


        }
    } else {
        const errorEle = document.createElement('h1');
        errorEle.textContent = 'unable to get past five match data';
        innerDiv.appendChild(errorEle);
    }

}



async function displayH2H(team1Name, team2Name){
    const placementContainer = document.getElementById('H2Hdata');

    const respond = await fetch('/head2head', {
        method: 'POST',
        body: JSON.stringify({ team1: team1Name, team2: team2Name }),
        headers: { 'Content-Type': 'application/json' }
    });

    const datas = await respond.json();
    if('datalist' in datas){
        const maxLength = Math.min(datas.match_outcome.length, datas.event_date.length, datas.team2_id.length);
        const dataList = datas['datalist'];
        for (let i = 0; i < maxLength; i++) {
            const divContainer = document.createElement('div');
            const textDiv = document.createElement('div')
            textDiv.className = 'textDiv';
            divContainer.className = '';
            const OutcomeText = document.createElement('h1');
            if (datas.match_outcome[i] === 'TeamOne') {
                OutcomeText.textContent = `outcome: Home win`;
            } else if (datas.match_outcome[i] === 'TeamTwo') {
                OutcomeText.textContent = `outcome: Away win`;
            } else {
                OutcomeText.textContent = 'outcome: draw';
            }
            const DateText = document.createElement('h1');
            DateText.textContent = `date: ${datas.event_date[i]}`;
            const teamText = document.createElement('h1');
            teamText.textContent = `team: ${datas.team1_id[i]} vs ${datas.team2_id[i]}`;

            textDiv.appendChild(OutcomeText);
            textDiv.appendChild(DateText);
            textDiv.appendChild(teamText);

            divContainer.appendChild(textDiv);

            placementContainer.appendChild(divContainer);
        }
    } else {
        const Message = document.createElement('h1');
        Message.textContent = 'unable to get Head-to-Head analysis';
        placementContainer.appendChild(Message);
    }
}



async function displayPFM(team1Name){
    const innerDiv = document.getElementById('homePFM');

    const respond = await fetch('/pastFiveMatch', {
        method: 'POST',
        body: JSON.stringify({ team1: team1Name }),
        headers: { 'Content-Type': 'application/json' }
    });

    const datas = await respond.json();
    if('win' in datas){
        const headerText = document.createElement('h1');
        headerText.textContent = team1Name;
        innerDiv.appendChild(headerText);
        const maxLength = Math.min(datas.win.length, datas.loss.length, datas.draw.length, datas.opponent.length, datas.outcome.length, datas.datepd.length);
        for(let i=0; i<maxLength; i++){
            const divContain = document.createElement('div');
            divContain.className = 'dataDisplay';
            const textDiv = document.createElement('div');
            textDiv.className = 'textDiv';
            const outcomeT = document.createElement('h1');
            outcomeT.textContent = `outcome: ${datas.outcome[i]}`;
            const opponentT = document.createElement('h1');
            opponentT.textContent = `opponent: ${datas.opponent[i]}`;
            const dateT = document.createElement('h1');
            dateT.textContent = `date: ${datas.datepd[i]}`;

            textDiv.appendChild(outcomeT);
            textDiv.appendChild(dateT);
            textDiv.appendChild(opponentT);

            const progressContainer = chart(datas.win[i], datas.loss[i], datas.draw[i]);
            innerDiv.appendChild(progressContainer);
            innerDiv.appendChild(textDiv);
        }
    } else {
        const errorEle = document.createElement('h1');
        errorEle.textContent = 'unable to get past five match data';
        innerDiv.appendChild(errorEle);
    }

}


async function displayPFMTWO(team2Name) {
    const innerDiv = document.getElementById('awayPFM');

    const respond = await fetch('/pastFiveMatch', {
        method: 'POST',
        body: JSON.stringify({ team1: team2Name }),
        headers: { 'Content-Type': 'application/json' }
    });

    const datas = await respond.json();
    if ('win' in datas) {
        const headerText = document.createElement('h1');
        headerText.textContent = team2Name;
        innerDiv.appendChild(headerText);
        const maxLength = Math.min(datas.win.length, datas.loss.length, datas.draw.length, datas.opponent.length, datas.outcome.length, datas.datepd.length);
        for (let i=0; i<maxLength; i++) {
            const divContain = document.createElement('div');
            divContain.className = 'dataDisplay';
            const textDiv = document.createElement('div');
            textDiv.className = 'textDiv';
            const outcomeT = document.createElement('h1');
            outcomeT.textContent = `outcome: ${datas.outcome[i]}`;
            const opponentT = document.createElement('h1');
            opponentT.textContent = `opponent: ${datas.opponent[i]}`;
            const dateT = document.createElement('h1');
            dateT.textContent = `date: ${datas.datepd[i]}`;

            textDiv.appendChild(outcomeT);
            textDiv.appendChild(dateT);
            textDiv.appendChild(opponentT);

            const progressContainer = chart(datas.win[i], datas.loss[i], datas.draw[i]);
            innerDiv.appendChild(progressContainer);
            innerDiv.appendChild(textDiv);
        }
    } else {
        const errorEle = document.createElement('h1');
        errorEle.textContent = 'unable to get past five match data';
        innerDiv.appendChild(errorEle);
    }

}



async function displayHAT(team1Name){
    const innerDiv = document.getElementById('homeAdvantage');
    
    const respond = await fetch('/homeAdvantages', {
        method: 'POST',
        body: JSON.stringify({ team1: team1Name }),
        headers: { 'Content-Type': 'application/json' }
    });
    
    const datas = await respond.json();
    if ('win' in datas){
        const headerText = document.createElement('h1');
        headerText.textContent = `${team1Name} home play`;
        innerDiv.appendChild(headerText);
        const maxLength = Math.min(datas.win.length, datas.loss.length, datas.draw.length, datas.opponent.length, datas.outcome.length, datas.date.length);
        for(let i=0; i<maxLength; i++){
            const divContain = document.createElement('div');
            divContain.className = 'dataDisplay';
            const textDiv = document.createElement('div');
            textDiv.className = 'textDiv';
            const outcomeT = document.createElement('h1');
            outcomeT.textContent = `outcome: ${datas.outcome[i]}`;
            const opponentT = document.createElement('h1');
            opponentT.textContent = `opponent: ${datas.opponent[i]}`;
            const dateT = document.createElement('h1');
            dateT.textContent = `date: ${datas.date[i]}`;

            textDiv.appendChild(outcomeT);
            textDiv.appendChild(dateT);
            textDiv.appendChild(opponentT);

            const progressContainer = chart(datas.win[i], datas.loss[i], datas.draw[i]);
            innerDiv.appendChild(progressContainer);
            innerDiv.appendChild(textDiv);
        }
    } else {
        const errorEle = document.createElement('h1');
        errorEle.textContent = 'unable to get home play data';
        innerDiv.appendChild(errorEle);
    }


}


async function displayAAT(team2Name) {
    const innerDiv = document.getElementById('awayAdvantage');
    
    const respond = await fetch('/awayadvantage', {
        method: 'POST',
        body: JSON.stringify({ team2: team2Name }),
        headers: { 'Content-Type': 'application/json' }
    });
    
    const datas = await respond.json();
    if ('win' in datas) {
        const headerText = document.createElement('h1');
        headerText.textContent = `${team2Name} away play`;
        innerDiv.appendChild(headerText);
        const maxLength = Math.min(datas.win.length, datas.loss.length, datas.draw.length, datas.opponent.length, datas.outcome.length, datas.date.length);
        for (let i = 0; i < maxLength; i++) {
            const divContain = document.createElement('div');
            divContain.className = 'dataDisplay';
            const textDiv = document.createElement('div');
            textDiv.className = 'textDiv';
            const outcomeT = document.createElement('h1');
            outcomeT.textContent = `outcome: ${datas.outcome[i]}`;
            const opponentT = document.createElement('h1');
            opponentT.textContent = `opponent: ${datas.opponent[i]}`;
            const dateT = document.createElement('h1');
            dateT.textContent = `date: ${datas.date[i]}`;

            textDiv.appendChild(outcomeT);
            textDiv.appendChild(dateT);
            textDiv.appendChild(opponentT);

            const progressContainer = chart(datas.win[i], datas.loss[i], datas.draw[i]);
            innerDiv.appendChild(progressContainer);
            innerDiv.appendChild(textDiv);
        }
    } else {
        const errorEle = document.createElement('h1');
        errorEle.textContent = 'unable to away play data';
        innerDiv.appendChild(errorEle);
    }


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
            await displayH2H(team1Selected, team2Selected);
            await displayHAT(team1Selected);
            await displayPFMTWO(team2Selected);
            await similarOppponet(team1Selected, team2Selected);
            await displayPFM(team1Selected);
            await displayAAT(team2Selected);
            loadings(false);
            throbber.style.display = 'none';
            alert('data received successfully');
        }
    }
}

function selecTion() {
    const selectPage = document.getElementById('optionPage');
    selectPage.style.display = 'flex';
}

let onlyHomeTeam = 'home team';
let onlyAwayTeam = 'away team';


function displayAnalysis(home, away) {
    fetch('/Analysis')
    .then(respond => respond.json())
    .then(data =>{
        window.location.href = data.redirect;
    })
    displayData(home, away);
}

function displayData(home, away){
    const h1Text = document.getElementById('HomeTeam');
    const h1TextTwo = document.getElementById('AwayTeam');
    const displayNow = document.getElementById('displayNow');

    h1Text.textContent = home;
    h1TextTwo.textContent = away;

    
}
