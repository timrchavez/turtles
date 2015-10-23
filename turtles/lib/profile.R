#!/usr/bin/Rscript
# Copyright 2015 Blue Box Cloud, an IBM Company
# Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# R script for generating a performance profile for an ansible playbook
# run

require("ggplot2")
require("scales")
require("grid")

# Default settings
title = "unset title"
subtitle = ""
datafile = "profile.csv"
imagefile = "profile.png"

# Override default settings
args <- commandArgs(trailingOnly = TRUE)
for(i in 1:length(args)){
    eval(parse(text=args[i]))
}

# Create data frame from data table
df <- read.csv2(datafile)
df$start <- as.POSIXct(strftime(df$start, "%Y-%m-%d %H:%M:%OS3"), tz="utc")
df$end <- as.POSIXct(strftime(df$end, "%Y-%m-%d %H:%M:%OS3"), tz="utc")
# HACK: Enforce ordering on Y-axis
df$event <- as.character(df$event)
df$event <- factor(df$event, levels=rev(unique(df$event)))

# Create the limits of a datetime continuum
padding <- 3600 * 1.5
limits <- c(head(df, 1)$start, tail(df,1)$end + padding)

# HACK: Prevent empty Rplot.pdf from being generated
options(device="png")
par()
dev.off()

# Color palette
colfunc<-colorRampPalette(c("hotpink","tomato1","springgreen","royalblue"))
# Generate plot
p <- ggplot(df, aes(colour = color)) +
    # Borrowed from: http://stackoverflow.com/questions/19957536/add-dynamic-subtitle-using-ggplot
    ggtitle(bquote(atop(.(title), atop(italic(.(subtitle)), "")))) +
    ylab("") +
    xlab("time (s)") +
    theme_minimal() +
    theme(legend.position = "none",
        text=element_text(colour = "white"),
        axis.text=element_text(size=5),
        axis.title=element_text(size=8, face="bold"),
        axis.line = element_blank(),
        axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size=5),
        axis.text.y = element_blank(),
        plot.background = element_rect(fill = "black"),
        panel.background = element_rect(fill = "black", colour = "black"),
        panel.border = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank()) +
    scale_colour_gradientn(colours = colfunc(tail(df,1)$color)) +
    scale_x_datetime(breaks = date_breaks("15 min"), labels = date_format("%R"), limits=limits) +
    geom_segment(aes(x = start, xend = end, y = event, yend = event), size = 1) +
    geom_text(aes(x = end, y = event, label = label), size = 1, hjust = -0.02) +
    ggsave(imagefile, height = par("din")[2] * 1.25)

