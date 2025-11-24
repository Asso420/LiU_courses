  for ( i = 0; i < LOOPS; ++i)
  {
    printf("Enter id to find value for: ");
    scanf("%d", &id);

    /*! find the value for a key in the map */
    obj = map_find(&container, id);
      if(obj != NULL)
      {
        printf("FOUND: %s\n", obj);
      }
      else {
        printf("Not found\n");
      }
    /*! if it was found, display it */
//YOUR CODE

    /* since we leave the value in the map we may use it again and
     * should not free the memory */
  }



    for ( i = 0; i < LOOPS; ++i)
  {
    printf("Enter id to remove value for: ");
    scanf("%d", &id);

    /*! find and remove a value for a key in the map */
    obj = map_remove(&container, id);

    /*! if it was found, display it */
      if(obj != NULL)
      {
        printf("REMOVED: %s\n", obj);
      }
      else {
        printf("Nothing to remove: \n");
      }
    /* since we removed the value from the map we will never use it again and
     * must properly free the memory (if it was allocated) */
  }

 printf("Will now display all values less than N. Choose N: ");
  scanf("%d", &i);
  map_for_each(&container, print_less, i);
  printf("\n");


  1 2 3 4 5 6 7 8 9 0