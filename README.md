# TrueSight

Hi! This is a project I'm working on to learn more about
AI-generated images and how to tell them apart from real photos.

I've always enjoyed drawing, so I've had mixed feelings about
AI-generated artwork. Some of it looks impressive, but it also
made me wonder what makes an AI-generated image different from
something made by a person.

That curiosity eventually led me to AI-image detection.
At first, I just wanted to understand how detectors work.
But the more I looked into it, the more I wondered what happens
when those detectors get things wrong.

I'm still learning, and this project is my way of exploring
these questions step by step.

## What I'm Exploring

Right now, I'm especially interested in how reliable
AI-image detectors are when they encounter images from
generators they haven't seen before.

The question I'm trying to understand is:

**Can a detector tell when its own prediction might be wrong?**

I'm starting with existing methods such as CNNDetection and
UniversalFakeDetect, rather than trying to build a new model
from scratch.

If I find something that doesn't work well, I'd like to
understand why and see whether there's a way to improve it.

## Where Things Stand

So far, the project includes:

- An early notebook for loading and displaying images.
- Notes on existing AI-image detection research.
- Plans for comparing detectors across different generators.
- A small Python evaluation tool for studying prediction errors
  and what happens when uncertain predictions are rejected.

The evaluation tool has passed 15 software tests using simulated
data. These tests only check the evaluation code.

**I haven't run real AI-image detector experiments yet.**

Some of the research organization, documentation, and code
have been developed with AI assistance. I've kept notes about
this in the research record.

## What's Next

The next step is to prepare a small dataset and test existing
detectors on real and AI-generated images.

I want to understand where they make mistakes, especially
when they seem confident about an incorrect answer.

If I can identify a consistent problem, I'll look into
existing solutions and try to improve one of them.

## Why This Repo Exists

I started this project because I was curious about AI images,
but I hope it also helps me learn how research actually works.

I'm still figuring out what area of AI I want to study more
seriously, and I think working through a real problem is
a good way to find out.

I'll try to keep track of what I learn, including experiments
that don't work as expected.

You can find the research notes and experiment plans in the
[research record](research/README.md).

Feedback and suggestions are always welcome!
