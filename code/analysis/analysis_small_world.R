library(ggplot2)
library(gridExtra)

# Shortcuts without storage; with chromatic number 
d.sw013 <- read.csv("../../data/data_small_world_s0_without_storage_item3.csv")
d.sw213 <- read.csv("../../data/data_small_world_s2_without_storage_item3.csv")
d.sw613 <- read.csv("../../data/data_small_world_s6_without_storage_item3.csv") 

d.sw013$network <- "Ring lattice"
d.sw213$network <- "2-shortcut\nring lattice"
d.sw613$network <- "6-shortcut\nring lattice"

ds1 <- rbind(d.sw013, d.sw213, d.sw613)
ds1$network <- factor(ds1$network, levels=c("Ring lattice", "2-shortcut\nring lattice", "6-shortcut\nring lattice"))
g1 <- ggplot(ds1, aes(x=network, y=1.0 - ave_rate/size)) +
  geom_boxplot() +
  ylim(0.0, 1.0) +
  labs(x="", y="% complete specialization") +
  theme_classic()


# Shortcuts without storage; with chromatic number 
d.sw023 <- read.csv("../../data/data_small_world_s0_with_storage_item3.csv")
d.sw223 <- read.csv("../../data/data_small_world_s2_with_storage_item3.csv")
d.sw623 <- read.csv("../../data/data_small_world_s6_with_storage_item3.csv") 

d.sw023$network <- "Ring lattice"
d.sw223$network <- "2-shortcut\nring lattice"
d.sw623$network <- "6-shortcut\nring lattice"

ds2 <- rbind(d.sw023, d.sw223, d.sw623)

ds2$network <- factor(ds2$network, levels=c("Ring lattice", "2-shortcut\nring lattice", "6-shortcut\nring lattice"))
g2 <- ggplot(ds2, aes(x=network, y=1.0 - ave_rate/size)) +
  geom_boxplot() +
  scale_y_continuous(limits=c(0.0, 1.0)) +
  labs(x="", y="% complete specialization") +
  theme_classic()


grid.arrange(g1, g2, ncol=2)

# Item number variation without storage capacity
d.sw013$num_item <- 3
d.sw213$num_item <- 3
d.sw613$num_item <- 3

d.sw012 <- read.csv("../../data/data_small_world_s0_without_storage_item2.csv")
d.sw212 <- read.csv("../../data/data_small_world_s2_without_storage_item2.csv")
d.sw612 <- read.csv("../../data/data_small_world_s6_without_storage_item2.csv") 

d.sw012$network <- "Ring lattice"
d.sw212$network <- "2-shortcut\nring lattice"
d.sw612$network <- "6-shortcut\nring lattice"

d.sw012$num_item <- 2
d.sw212$num_item <- 2
d.sw612$num_item <- 2

d.sw014 <- read.csv("../../data/data_small_world_s0_without_storage_item4.csv")
d.sw214 <- read.csv("../../data/data_small_world_s2_without_storage_item4.csv")
d.sw614 <- read.csv("../../data/data_small_world_s6_without_storage_item4.csv") 

d.sw014$network <- "Ring lattice"
d.sw214$network <- "2-shortcut\nring lattice"
d.sw614$network <- "6-shortcut\nring lattice"

d.sw014$num_item <- 4
d.sw214$num_item <- 4
d.sw614$num_item <- 4

ds01 <- rbind(d.sw013, d.sw012, d.sw014)
ds01$num_item2 <- factor(ds01$num_item, level=c(2, 3, 4), labels=c("2 items", "3 items\nchromatic\nnumber", "4 items"))
g1 <- ggplot(ds01, aes(x=num_item2, y=1 - ave_rate/42)) +
  geom_boxplot() +
  scale_y_continuous(limits=c(0.0, 1.0)) +
  labs(x="", y="% complete specialization") +
  theme_classic()

ds21 <- rbind(d.sw213, d.sw212, d.sw214)
ds21$num_item2 <- factor(ds21$num_item, level=c(2, 3, 4), labels=c("2 items", "3 items\nchromatic\nnumber", "4 items"))
g2 <- ggplot(ds21, aes(x=num_item2, y=1 - ave_rate/42)) +
  geom_boxplot() +
  scale_y_continuous(limits=c(0.0, 1.0)) +
  labs(x="", y="% complete specialization") +
  theme_classic()

ds61 <- rbind(d.sw613, d.sw612, d.sw614)
ds61$num_item2 <- factor(ds61$num_item, level=c(2, 3, 4), labels=c("2 items", "3 items\nchromatic\nnumber", "4 items"))
g3 <- ggplot(ds61, aes(x=num_item2, y=1 - ave_rate/42)) +
  geom_boxplot() +
  scale_y_continuous(limits=c(0.0, 1.0)) +
  labs(x="", y="% complete specialization") +
  theme_classic()

grid.arrange(g1, g2, g3, ncol=3)
