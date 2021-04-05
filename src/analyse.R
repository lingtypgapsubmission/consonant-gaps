# Gap counts by inventory sizes

library(ggplot2)
library(cowplot)  # For several ggplots on one sheet

d <- read.csv('../csv/gap_count_inv_size.csv')

p1 <- ggplot(aes(x = InventorySize, y = GapCount), data = d) + 
    geom_point() + 
    geom_smooth(method = "loess") +
    theme_bw()
p2 <- ggplot(aes(x = InventorySize, y = GapCount / InventorySize), data = d) + 
    geom_point() + 
    geom_smooth(method = "loess") +
    theme_bw()

png(
    '../plots/gap_count_inv_size.png',
    width = 16,
    height = 20,
    units = 'in',
    res = 300
)
par(mfrow = c(2,1))
plot_grid(p1, p2, nrow = 2, labels = c(
    'A',
    'B'
))
dev.off()

png(
    '../plots/gap_count_inv_size_proportional.png',
    width = 16,
    height = 10,
    units = 'in',
    res = 300
)
ggplot(aes(x = InventorySize, y = GapCount / InventorySize), data = d) + 
    geom_point() + 
    geom_smooth(method = "loess") +
    theme_bw()
dev.off()

# In and between-class fricative gaps.

library(xtable)

d2 <- read.csv('../csv/fricative_gaps_in_between.csv')
d2s = d2[order(d2$InClass, na.last = TRUE, decreasing = T),]
print(
    xtable(t(d2s[
        (d2s$InClass > 4) & (d2s$Both == 0) & (d2s$BetweenClass == 0),
        c('Phoneme', 'InClass')
    ])), include.colnames=F)

print(
    xtable(t(d2[
        (d2$BetweenClass >= 5) & (d2$Both == 0) & (d2$InClass == 0),
        c('Phoneme', 'BetweenClass')
    ])), include.colnames=F)

d2test = d2[(d2$Both > 0) | (d2$InClass > 0),]

print(
    xtable(t(d2s[
        (d2s$BetweenClass >= 10) & ((d2s$Both > 0) | (d2s$InClass > 0)),
        c('Phoneme', 'BetweenClass')
    ])), include.colnames=F)


stopd <- read.csv('../csv/stop_gaps_in_between.csv')
stop.in <- stopd[
            (stopd$InClass > 4) & (stopd$Both == 0) & (stopd$BetweenClass == 0),
            c('Phoneme', 'InClass')
        ]
print(
    xtable(t(
        stop.in[order(stop.in$InClass, decreasing = T),]        
    )), include.colnames=F)

stops <- stopd[order(stopd$BetweenClass, decreasing = T),]
print(xtable(stops[
    ( (stops$InClass > 0) | (stops$Both > 0) ) & (stops$BetweenClass >= 10),
    ]), include.rownames=F)
print(
    xtable(t(
        stopd[order(stopd$BetweenClass, decreasing = T),]        
    )), include.colnames=F)