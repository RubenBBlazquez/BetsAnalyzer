db.createUser(
    {
        "user": "bets_analyzer",
        "pwd": "bets_analyzer",
        "roles": [
            {
                "role": "readWrite",
                "db": "admin"
            }
        ]
    }
);
