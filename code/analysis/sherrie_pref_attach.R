library(ggplot2)
library(scales)
library(lme4)
library(gridExtra)

pa212 <- read.csv("../../data/data_pref_attach_2_without_storage_item2.csv")
pa212$num_item <- 2
pa213 <- read.csv("../../data/data_pref_attach_2_without_storage_item3.csv")
pa213$num_item <- 3
pa214 <- read.csv("../../data/data_pref_attach_2_without_storage_item4.csv")
pa214$num_item <- 4

pa313 <- read.csv("../../data/data_pref_attach_3_without_storage_item3.csv")
pa313$num_item <- 3
pa314 <- read.csv("../../data/data_pref_attach_3_without_storage_item4.csv")
pa314$num_item <- 4
pa315 <- read.csv("../../data/data_pref_attach_3_without_storage_item5.csv")
pa315$num_item <- 5

pa223 <- read.csv("../../data/data_pref_attach_2_with_storage_item3.csv")
pa223$num_item <- 3
pa324 <- read.csv("../../data/data_pref_attach_3_with_storage_item4.csv")
pa324$num_item <- 4

# Item number
dd2 <- rbind(pa212, pa213, pa214)
dd2$num_item2 <- factor(dd2$num_item, level=c(2, 3, 4), labels=c("2 items", "3 items\nchromatic\nnumber", "4 items"))
g1 <- ggplot(dd2, aes(x=num_item2, y=1 - ave_rate)) +
  geom_boxplot() +
  scale_y_continuous(limits=c(0.0, 1.0)) +
  labs(x="", y="% complete specialization") +
  theme_classic()

dd3 <- rbind(pa313, pa314, pa315)
dd3$num_item2 <- factor(dd3$num_item, level=c(3, 4, 5), labels=c("3 items", "4 items\nchromatic\nnumber", "5 items"))
g2 <- ggplot(dd3, aes(x=num_item2, y=1 - ave_rate)) +
  geom_boxplot() +
  scale_y_continuous(limits=c(0.0, 1.0)) +
  labs(x="", y="% complete specialization") +
  theme_classic()

grid.arrange(g1, g2, ncol=2)

# Solution number without storage; with chromatic number 
g1 <- ggplot(pa213, aes(x=X.solutions, y=1-ave_rate)) +
  geom_point(size=0.8, alpha=0.6) +
  scale_x_log10(breaks = c(10, 100, 1000),
                labels = trans_format("log10", math_format(10^.x))) +
  scale_y_continuous(breaks=seq(0, 1.0, 0.2), limits = c(0.0, 1.0)) +
  labs(x="Chromatic solution number", y="% complete specialization") +
  theme_classic()

cor.test(log10(pa213$X.solutions), 1-pa213$ave_rate)

g2 <- ggplot(pa314, aes(x=X.solutions, y=1.0 - ave_rate)) +
  geom_point(size=0.8, alpha=0.6) +
  scale_x_log10(breaks = c(1000, 10000, 100000, 1000000),
                labels = trans_format("log10", math_format(10^.x))) +
  scale_y_continuous(breaks=seq(0, 1.0, 0.2), limits = c(0.0, 1.0)) +
  labs(x="Chromatic solution number", y="% complete specialization") +
  theme_classic()

cor.test(log10(pa314$X.solutions), 1-pa314$ave_rate)

grid.arrange(g1, g2, ncol=2)

# Solution number with storage; with chromatic number
g1 <- ggplot(pa223, aes(x=X.solutions, y=1.0 - ave_rate)) +
  geom_point(size=0.8, alpha=0.6) +
  scale_x_log10(breaks = c(10, 100, 1000),
                labels = trans_format("log10", math_format(10^.x))) +
  scale_y_continuous(breaks=seq(0, 1.0, 0.2), limits = c(0.0, 1.0)) +
  labs(x="Chromatic solution number", y="% complete specialization") +
  theme_classic()

cor.test(log10(pa223$X.solutions), 1 - pa223$ave_rate)

g2 <- ggplot(pa324, aes(x=X.solutions, y=1.0 - ave_rate)) +
  geom_point(size=0.8, alpha=0.6) +
  scale_x_log10(breaks = c(1000, 10000, 100000, 1000000),
                labels = trans_format("log10", math_format(10^.x))) +
  scale_y_continuous(breaks=seq(0, 1.0, 0.2), limits = c(0.0, 1.0)) +
  labs(x="Chromatic solution number", y="% complete specialization") +
  theme_classic()

cor.test(log10(pa324$X.solutions), 1 - pa324$ave_rate)

grid.arrange(g1, g2, ncol=2)

#Linear regression
pa20 <- read.csv("../../data/data_pref_attach_2_base.csv")

d21 <- merge(pa213, pa20, by="gameId")
fit21 <- lm((1.0-ave_rate)  ~ scale(log10(X.solutions.x)) + scale(clustering) + scale(shortest_path), data=d21)
summary(fit2.1)

d22 <- merge(pa223, pa20, by="gameId")
fit22 <- lm((1.0-ave_rate)  ~ scale(log10(X.solutions.x)) + scale(clustering) + scale(shortest_path), data=d22)
summary(fit2.2)

pa30 <- read.csv("../../data/data_pref_attach_3_base.csv") 

d31 <- merge(pa314, pa30, by="gameId")
fit31 <- lm((1.0-ave_rate)  ~ scale(log10(X.solutions.x)) + scale(clustering) + scale(shortest_path), data=d31)
summary(fit3.1)

d32 <- merge(pa324, pa30, by="gameId")
fit32 <- lm((1.0-ave_rate) ~ scale(log10(X.solutions.x)) + scale(clustering) + scale(shortest_path), data=d32)
summary(fit3.2)
