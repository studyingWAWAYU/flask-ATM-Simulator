
document.addEventListener("DOMContentLoaded", () => {
    const joinClubButton = document.querySelectorAll('.join-club-btn');
    joinClubButton.forEach(button => {
        button.addEventListener('click', function () {
            const confirmation = confirm("Are you sure you want to join this club?");
            if (!confirmation) {
                return;
            }
            const club_id = this.dataset.clubId;
            fetch(`/joinClub`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({club_id: club_id})
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                } else if (data.error) {
                    alert(data.error);
                }
            });
        });
    });
});