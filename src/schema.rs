table! {
    matches (hash_id) {
        hash_id -> Varchar,
        team_1 -> Nullable<Varchar>,
        team_2 -> Nullable<Varchar>,
        team_1_score -> Nullable<Int4>,
        team_2_score -> Nullable<Int4>,
        tournament -> Nullable<Varchar>,
        matchtype -> Nullable<Varchar>,
        match_time -> Nullable<Int4>,
    }
}

table! {
    odds (team_1, team_2, scrape_time, match_time, source) {
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

allow_tables_to_appear_in_same_query!(
    matches,
    odds,
);
