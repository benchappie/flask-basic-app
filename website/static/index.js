function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST", 
        body: JSON.stringify({ noteId: noteId }), 
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteSet(setId) {
    fetch("/delete-set", {
        method: "POST", 
        body: JSON.stringify({ setId: setId }), 
    }).then((_res) => {
        window.location.href = "/workout";
    });
}

