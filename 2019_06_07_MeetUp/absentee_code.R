library('tidyverse')
library('sf')

options(device = "X11")
X11.options(type = "cairo")

counties <- "input/Maryland_Physical_Boundaries__County_Boundaries_Generalized/Maryland_Physical_Boundaries__County_Boundaries_Generalized.shp"
counties.read <- st_read(counties)

output <- read_csv('output/output.csv')

output <- output %>% mutate(cand = case_when(candidate == 'Ben  Jealous and Susan  Turnbull' ~ 'jealous',
                                             candidate == 'Larry  Hogan and Boyd K. Rutherford' ~ 'hogan',
                                             candidate == 'Ian  Schlakman and Annie  Chambers' ~ 'schlakman',
                                             candidate == 'Shawn  Quinn and Christina  Smith' ~ 'quinn',
                                             candidate == 'Other Write-Ins' ~ 'write_in'))

output <- output %>% group_by(county) %>% mutate(max_vote = max(absentee_vote),
                                                 total_abs_vote = sum(absentee_vote),
                                                 abs_perc = absentee_vote/total_abs_vote * 100)

output_wide <- output %>% spread(key = cand, value = absentee_vote)

output_wide <- output_wide %>% group_by(county) %>% mutate(jealous = max(jealous, na.rm = T),
                                                           hogan = max(hogan, na.rm = T),
                                                           schlakman = max(schlakman, na.rm = T),
                                                           quinn = max(quinn, na.rm = T),
                                                           write_in = max(write_in, na.rm = T))

output_wide <- output_wide %>% select(county, max_vote, total_abs_vote, jealous, hogan, schlakman, quinn, write_in) %>% distinct()

output_wide <- output_wide %>% mutate(abs_winner = case_when(max_vote == jealous ~ 'jealous',
                                                             max_vote == hogan ~ 'hogan',
                                                             max_vote == schlakman ~ 'schlakman',
                                                             max_vote == write_in ~ 'write_in'))

output_wide <- output_wide %>% mutate(perc_jealous = jealous / total_abs_vote * 100,
                                      perc_hogan = hogan / total_abs_vote * 100,
                                      perc_schlakman = schlakman / total_abs_vote * 100,
                                      perc_quinn = quinn / total_abs_vote * 100,
                                      perc_write_in = write_in / total_abs_vote * 100,
                                      perc_winner = max_vote / total_abs_vote * 100)

counties.merge <- merge(counties.read, output_wide, by = 'county', all = T)

counties.merge <- counties.merge %>% mutate(perc_jealous = signif(perc_jealous, 2),
                                            perc_hogan = signif(perc_hogan, 2),
                                            perc_schlakman = signif(perc_schlakman, 2),
                                            perc_quinn = signif(perc_quinn, 2),
                                            perc_write_in = signif(perc_write_in, 2),
                                            perc_winner = max_vote / total_abs_vote * 100)

counties.merge <- counties.merge %>% mutate(cat = case_when(perc_winner >= 49 & perc_winner <= 55 ~ 1,
                                                            perc_winner > 55 & perc_winner <= 65 ~ 2,
                                                            perc_winner > 65 & perc_winner <= 75 ~ 3,
                                                            perc_winner >= 75 ~ 4), 
                                            perc_cats_map = ifelse(abs_winner == 'jealous', cat * -1, 
                                                                   cat))

ggplot() + geom_sf(data = counties.merge, 
                   aes(fill = perc_cats_map)) + 
  scale_fill_gradient2(low = "#007dbe", mid = "white",
                       high = "#b8292f", space = "Lab", midpoint = 0,
                       na.value = "#afafaf", guide = "legend", 
                       aesthetics = "fill") +
  theme_void() +
  theme(panel.grid.major = element_line(colour = 'transparent')) 

st_write(counties.merge, 'output/counties_merge_absentee.shp')
