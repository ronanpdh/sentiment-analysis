const messages = {
    array1: [
       "Write about a time when ",
       "Describe an experience where ",
       "Reflect on a moment when ",
       "Explore a scenario where ",
       "Recount a day when ",
       "Illustrate an instance when ",
       "Delve into a situation where ",
       "Narrate a circumstance when "
   ],
   
    array2: [
       "you faced a challenge ",
       "you felt genuine happiness ",
       "you learned something new ",
       "you overcame a fear ",
       "you helped someone in need ",
       "you made a tough decision ",
       "you discovered a passion ",
       "you formed a meaningful relationship "
   ],
   
    array3:[
       "and how it shaped your perspective.",
       "and what it taught you about yourself.",
       "and how it influenced your future decisions.",
       "and the emotions it evoked in you.",
       "and how it impacted those around you.",
       "and the lessons you drew from it.",
       "and its long-term effects on your life.",
       "and how it contributed to your personal growth."
   ]
}

// create event variables 
let promptOutput = document.getElementById('prompt');
let promptBtn = document.getElementById('generator');

// Event Handler to generate prompts
promptBtn.addEventListener('click', function(){
   let random1 = Math.floor(Math.random() * messages.array1.length); 
   let random2 = Math.floor(Math.random() * messages.array2.length); 
   let random3 = Math.floor(Math.random() * messages.array3.length); 
   let prompt1 = messages.array1[random1];
   let prompt2 = messages.array2[random2];
   let prompt3 = messages.array3[random3];
   promptOutput.innerHTML = prompt1 + prompt2 + prompt3;
   console.log(prompt1 + prompt2 + prompt3)
}); 
