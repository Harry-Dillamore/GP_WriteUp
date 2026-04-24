# Game description

## Overview

We are working in a large team of developers, designers, artists, animators, and musicians. And we are using Unreal engine with Git for version control.
The game is called 'Greedy Piggies' and is a multiplayer card game similar to 'liar's bar' where the aim of the game is to earn the most in game currency. The game loop is:
- Players are dealt hands of 5 cards
- The current player puts down 3 cards and makes a claim of what value they add up to
- Other players can 'audit' them if they think that they are lying
- If the auditor wins the current player loses the declared value
- If the current player wins the auditor loses the declared value
- If the current player doesn't get audited they win the declared value
- The game ends when someone reaches 250,000 currency
- Players are eliminated when they drop below -50,000 currency

## Scoring

- Cards are worth 1000x their face value
- If pairs of cards are put down their value is doubled
- If three of a kind are put down their value is tripled

## Shop Cards

- Every 3 rounds a shop phase begins
- Players can buy cards with their in game currency
- The cards all have unique abilities that can be used to help the player

# My Role

I am a lead developer on the game and am responsible for creating the core gameplay loop, and setting up systems for the shop and abilities which will make it easy for our large team of designers to create new cards and abilities.

The main tool I have worked on is an in editor tool for creating the files for new cards and abilities. I put time into this because I felt that it would help to create a system where many people can work on separate cards at the same time, but have a unified system for managing all of the cards.

I am also responsible for managing the git repository for the project, and ensuring that there are minimal conflicts when multiple people are working on the game.