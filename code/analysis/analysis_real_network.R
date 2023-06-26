library(ggplot2)
library(scales)
library(gridExtra)

d <- read.csv("../../data/data_real_network.csv")

d$rate <- 1- d$rate_completion / d$num_node
d$f_threshold <- factor(d$threshold)

dd1 <- subset(d, f_threshold==0)
g1 <- ggplot(dd1, aes(x=X.step, y=rate, color=group, group=group)) +
  geom_line(size=0.8) +
  scale_x_continuous( limits = c(0, 500)) +
  scale_y_continuous(breaks=seq(0, 1.0, 0.25), limits = c(0.0, 1.0)) +
  labs(x="Step", y="% complete specialization") +
  scale_colour_grey(start=0.8, end=0.2) +
  theme_classic() +
  theme(
    legend.position = "none"
  )

dd2 <- subset(d, f_threshold==10000)
g2 <- ggplot(dd2, aes(x=X.step, y=rate, color=group, group=group)) +
  geom_line(size=0.8) +
  scale_x_continuous( limits = c(0, 500)) +
  scale_y_continuous(breaks=seq(0, 1.0, 0.25), limits = c(0.0, 1.0)) +
  labs(x="Step", y="% complete specialization") +
  scale_colour_grey(start=0.8, end=0.2) +
  theme_classic() +
  theme(
    legend.position = "none"
  )
grid.arrange(g1, g2, ncol=2)
