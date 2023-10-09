<script>
  import "../app.postcss";
  import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
  import { storePopup } from '@skeletonlabs/skeleton';
  import { alertState } from '$lib/alertStore';
  storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

  let alertHideTimeout = null;

  alertState.subscribe((currState) => {
      if(currState.visible){
          alertHideTimeout = setTimeout(() =>{
              alertState.hide();
          },2500);
      }else{
          clearTimeout(alertHideTimeout);
      }
  });



</script>

{#if $alertState.visible}
    {#if $alertState.type === "error"}
        <aside class="alert variant-filled-error w-3/4 absolute top-[90%] left-1/2 -translate-x-1/2 -translate-y-1/2 h-auto">
            <div class="alert-message">
                {$alertState.message}
            </div>
            <div class="alert-actions"><button class="btn variant-filled font-bold" on:click={alertState.hide}>X</button></div>
        </aside>
        {:else if $alertState.type === "warning"}
        <aside class="alert variant-filled-warning w-3/4 absolute top-[90%] left-1/2 -translate-x-1/2 -translate-y-1/2 h-auto">
            <div class="alert-message">
                {$alertState.message}
            </div>
            <div class="alert-actions"><button class="btn variant-filled font-bold" on:click={alertState.hide}>X</button></div>
        </aside>
    {/if}


{/if}



<slot />
