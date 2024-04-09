
function getSelectedTeams(){
    const selectedTeam1 = document.getElementById('Team1');
    const selectedTeam2 = document.getElementById('Team2');
    const team1Selected = selectedTeam1.value;
    const team2Selected = selectedTeam2.value;

    if(team1Selected, team2Selected){
        fetch('/home', {
            method: 'POST',
            body: JSON.stringify({team1: team1Selected, team2: team2Selected}),
            headers: {'Content-Type': 'application/json'}
        })
        .catch(error => {
            alert(error);
        })
    }
}