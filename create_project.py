import os
import zipfile
import shutil

# --- Project Details ---
PROJECT_NAME = "todo-app"
FILES = {
    # Maven Project File
    "pom.xml": """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.4</version> <relativePath/> </parent>
    <groupId>com.example</groupId>
    <artifactId>todo-app</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>todo-app</name>
    <description>A simple to-do list application using Spring Boot and MySQL.</description>
    <properties>
        <java.version>17</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
""",

    # Application Configuration
    "src/main/resources/application.properties": """# MySQL Database Connection
spring.datasource.url=jdbc:mysql://localhost:3306/todo_db?useSSL=false&serverTimezone=UTC
spring.datasource.username=your_mysql_username
spring.datasource.password=your_mysql_password

# JPA/Hibernate Configuration
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect
""",

    # Main Spring Boot Application Class
    "src/main/java/com/example/todoapp/TodoAppApplication.java": """package com.example.todoapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TodoAppApplication {

    public static void main(String[] args) {
        SpringApplication.run(TodoAppApplication.class, args);
    }

}
""",

    # Model (Entity)
    "src/main/java/com/example/todoapp/model/Todo.java": """package com.example.todoapp.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "todos")
public class Todo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String task;

    private boolean completed = false;

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTask() {
        return task;
    }

    public void setTask(String task) {
        this.task = task;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }
}
""",

    # Repository
    "src/main/java/com/example/todoapp/repository/TodoRepository.java": """package com.example.todoapp.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.example.todoapp.model.Todo;

@Repository
public interface TodoRepository extends JpaRepository<Todo, Long> {
}
""",

    # Controller
    "src/main/java/com/example/todoapp/controller/TodoController.java": """package com.example.todoapp.controller;

import com.example.todoapp.model.Todo;
import com.example.todoapp.repository.TodoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/todos")
@CrossOrigin(origins = "*")
public class TodoController {

    @Autowired
    private TodoRepository todoRepository;

    @GetMapping
    public List<Todo> getAllTodos() {
        return todoRepository.findAll();
    }

    @PostMapping
    public Todo createTodo(@RequestBody Todo todo) {
        return todoRepository.save(todo);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Todo> updateTodo(@PathVariable Long id, @RequestBody Todo todoDetails) {
        Optional<Todo> optionalTodo = todoRepository.findById(id);
        if (optionalTodo.isPresent()) {
            Todo existingTodo = optionalTodo.get();
            existingTodo.setTask(todoDetails.getTask());
            existingTodo.setCompleted(todoDetails.isCompleted());
            return ResponseEntity.ok(todoRepository.save(existingTodo));
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTodo(@PathVariable Long id) {
        if (todoRepository.existsById(id)) {
            todoRepository.deleteById(id);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
""",

    # Simple Frontend
    "src/main/resources/static/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spring Boot To-Do App</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
        .container { max-width: 600px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #4a4a4a; }
        #todo-form { display: flex; margin-bottom: 20px; }
        #task-input { flex-grow: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        #add-btn { padding: 10px 15px; border: none; background-color: #5c67f2; color: white; border-radius: 4px; margin-left: 10px; cursor: pointer; }
        ul { list-style-type: none; padding: 0; }
        li { display: flex; align-items: center; padding: 10px; border-bottom: 1px solid #eee; }
        li.completed span { text-decoration: line-through; color: #999; }
        li span { flex-grow: 1; cursor: pointer; }
        .delete-btn { padding: 5px 10px; border: none; background-color: #e57373; color: white; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>To-Do List ✅</h1>
        <form id="todo-form">
            <input type="text" id="task-input" placeholder="Enter a new task..." required>
            <button type="submit" id="add-btn">Add Task</button>
        </form>
        <ul id="todo-list"></ul>
    </div>
    <script>
        const API_URL = 'http://localhost:8080/api/todos';
        const todoForm = document.getElementById('todo-form');
        const taskInput = document.getElementById('task-input');
        const todoList = document.getElementById('todo-list');

        async function fetchTodos() {
            const response = await fetch(API_URL);
            const todos = await response.json();
            todoList.innerHTML = '';
            todos.forEach(todo => {
                const li = document.createElement('li');
                li.dataset.id = todo.id;
                if (todo.completed) {
                    li.classList.add('completed');
                }
                const span = document.createElement('span');
                span.textContent = todo.task;
                span.addEventListener('click', () => toggleComplete(todo));
                const deleteBtn = document.createElement('button');
                deleteBtn.textContent = 'Delete';
                deleteBtn.classList.add('delete-btn');
                deleteBtn.addEventListener('click', () => deleteTodo(todo.id));
                li.appendChild(span);
                li.appendChild(deleteBtn);
                todoList.appendChild(li);
            });
        }

        todoForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const task = taskInput.value.trim();
            if (!task) return;
            await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task: task, completed: false })
            });
            taskInput.value = '';
            fetchTodos();
        });

        async function toggleComplete(todo) {
            await fetch(`${API_URL}/${todo.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...todo, completed: !todo.completed })
            });
            fetchTodos();
        }

        async function deleteTodo(id) {
            await fetch(`${API_URL}/${id}`, {
                method: 'DELETE'
            });
            fetchTodos();
        }
        fetchTodos();
    </script>
</body>
</html>
"""
}

# --- Script Logic ---
def create_project():
    """Creates the project structure, zips it, and cleans up."""
    print(f"Creating project structure for '{PROJECT_NAME}'...")

    # Create all files and directories
    for path, content in FILES.items():
        full_path = os.path.join(PROJECT_NAME, path)
        dir_name = os.path.dirname(full_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Project files created successfully.")

    # Zip the created directory
    zip_filename = f"{PROJECT_NAME}.zip"
    print(f"Creating zip file: {zip_filename}...")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(PROJECT_NAME):
            for file in files:
                file_path = os.path.join(root, file)
                archive_name = os.path.relpath(file_path, start=PROJECT_NAME)
                zipf.write(file_path, arcname=archive_name)

    print(f"'{zip_filename}' created successfully.")

    # Clean up the temporary project directory
    print(f"Cleaning up temporary directory '{PROJECT_NAME}'...")
    shutil.rmtree(PROJECT_NAME)
    print("Cleanup complete.")
    print("\n✅ All done! You can now extract and use your zip file.")


if __name__ == "__main__":
    create_project()