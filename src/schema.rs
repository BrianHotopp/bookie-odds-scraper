table! {
    matches (team_1, team_2, scrape_time, match_time, source) {
        team_1 -> Varchar,
        team_2 -> Varchar,
        team_1_winner_odds -> Nullable<Numeric>,
        team_2_winner_odds -> Nullable<Numeric>,
        draw_odds -> Nullable<Numeric>,
        bet_type -> Nullable<Varchar>,
        scrape_time -> Int4,
        match_time -> Int4,
        tournament_name -> Nullable<Varchar>,
        source -> Varchar,
    }
}
