flowchart TD
    Start([Inicio]) --> Menu{Menú Principal}
    Menu -->|Ver Películas| ViewMovies[Listar Películas]
    Menu -->|Agregar Película| AddMovie[Agregar Nueva Película]
    Menu -->|Buscar Película| SearchMovie[Buscar por Título]
    Menu -->|Eliminar Película| DeleteMovie[Eliminar Película]
    Menu -->|Salir| End([Fin])
    
    ViewMovies --> DisplayList[Mostrar Lista Completa]
    DisplayList --> Menu
    
    AddMovie --> InputDetails[Ingresar Detalles]
    InputDetails --> SaveMovie[Guardar en BD]
    SaveMovie --> ConfirmAdd{¿Agregar otra?}
    ConfirmAdd -->|Sí| AddMovie
    ConfirmAdd -->|No| Menu
    
    SearchMovie --> InputTitle[Ingresar Título]
    InputTitle --> SearchDB[Buscar en BD]
    SearchDB --> Found{¿Encontrada?}
    Found -->|Sí| ShowResult[Mostrar Resultado]
    Found -->|No| NotFound[No se encontró]
    ShowResult --> Menu
    NotFound --> Menu
    
    DeleteMovie --> InputID[Ingresar ID]
    InputID --> ConfirmDelete{¿Confirmar eliminación?}
    ConfirmDelete -->|Sí| RemoveMovie[Eliminar de BD]
    ConfirmDelete -->|No| Menu
    RemoveMovie --> Menu
    
    classDef processStyle stroke:#818cf8,fill:#eef2ff
    classDef decisionStyle stroke:#fb923c,fill:#fff7ed
    classDef startEndStyle stroke:#4ade80,fill:#f0fdf4
    classDef dataStyle stroke:#a78bfa,fill:#f5f3ff
    
    class Start,End startEndStyle
    class Menu,Found,ConfirmAdd,ConfirmDelete decisionStyle
    class ViewMovies,AddMovie,SearchMovie,DeleteMovie,InputDetails,SaveMovie,InputTitle,SearchDB,ShowResult,NotFound,InputID,RemoveMovie,DisplayList processStyle
    class SearchDB,SaveMovie dataStyle