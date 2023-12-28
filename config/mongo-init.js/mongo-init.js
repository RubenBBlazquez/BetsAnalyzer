db.createUser(
    {
        "user": "admin",
        "pwd": "bets_analyzer",
        "roles": [
            {
                "role": "readWrite",
                "db": "admin"
            }
        ]
    }
);
