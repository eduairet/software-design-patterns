# Introduction

## What is a Design Pattern?

A design pattern is a general reusable solution to a commonly occurring problem within a given context in software design. It is not a finished design that can be transformed directly into code. It is a description or template for how to solve a problem that can be used in many different situations.

## Why Use Design Patterns?

Design patterns can speed up the development process by providing tested, proven development paradigms. Effective software design requires considering issues that may not become visible until later in the implementation. Reusing design patterns helps to prevent subtle issues that can cause major problems and improves code readability for coders and architects who are familiar with the patterns.

## SOLID Principles

The SOLID principles are five principles of object-oriented programming intended to make software designs more understandable, flexible, and maintainable.

- **Single Responsibility Principle (SRP)**: A class should have only one reason to change, meaning that a class should have only one job.
- **Open/Closed Principle (OCP)**: Software entities should be open for extension but closed for modification.
- **Liskov Substitution Principle (LSP)**: Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program.
- **Interface Segregation Principle (ISP)**: A client should never be forced to implement an interface that it doesn't use, or clients shouldn't be forced to depend on interfaces they do not use.
- **Dependency Inversion Principle (DIP)**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

## Types of Design Patterns

- Gamma categorization is a way to group design patterns based on their intent or purpose, the three categories are:

  - **Creational Patterns**: These design patterns deal with object creation mechanisms, trying to create objects in a manner suitable to the situation. The basic form of object creation could result in design problems or added complexity to the design. Creational design patterns solve this problem by controlling the object creation process.
  - **Structural Patterns**: These design patterns deal with object composition. They describe how classes and objects can be composed to form larger structures. Structural design patterns simplify the structure by identifying the relationships.
  - **Behavioral Patterns**: These design patterns deal with object collaboration. They describe how objects interact to fulfill a task. Behavioral patterns are concerned with algorithms and the assignment of responsibilities between objects.

## References

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/)
